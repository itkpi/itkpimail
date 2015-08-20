import logging
import json
from django.http import HttpResponse, Http404, JsonResponse
from django.template import Template, Context
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from events.models import SuggestedEvent
from hooks.models import Hook, IncomingHook, IN_EVENT_SUGGEST
import requests
import trafaret as t

logger = logging.getLogger(__name__)


def call_hook(event_name, instance):
    for hook in Hook.objects.filter(event=event_name):
        logger.debug("Hook called: making {} request to {}".format(hook.method, hook.url))
        if hook.method == 'POST':
            data = Template(hook.body).render(Context({'object': instance}))
            requests.post(hook.url, data.encode('utf-8'))
        else:
            requests.request(hook.method, hook.url)


class IncomingHookView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, key):
        try:
            self.hook = IncomingHook.all_objects.get(key=key)
        except IncomingHook.DoesNotExist:
            return JsonResponse(status=404, data={"status": "wrong key"})
        if self.hook.event == IN_EVENT_SUGGEST:
            try:
                data = json.loads(request.body.decode())
            except ValueError as v:
                return JsonResponse(status=400, data={"status": "invalid json", "error": str(v)})
            return self.event_suggested(data)
        return HttpResponse('ok')

    def event_suggested(self, data):
        c = t.Dict({t.Key(name='title'): t.String,
                    t.Key(name='agenda'): t.String,
                    t.Key(name='social'): t.String,
                    t.Key(name='image_url'): t.URL,
                    t.Key(name='level'): t.String,
                    t.Key(name='place', optional=True): t.String,
                    t.Key(name='when'): t.String(regex='^(\d+)-(\d+)-(\d+)$'),
                    t.Key(name='when_time', optional=True): t.String(regex='^(\d+):(\d+)$'),
                    t.Key(name='when_end', optional=True): t.String(regex='^(\d+)-(\d+)-(\d+)$'),
                    t.Key(name='when_end_time', optional=True): t.String(regex='^(\d+):(\d+)$'),
                    t.Key(name='registration', optional=True): t.URL}
                   ) >> (lambda d: SuggestedEvent(**d))
        try:
            event = c.check(data)
        except t.DataError as e:
            return JsonResponse(status=400, data={"status": "data error", "error": str(e)})
        event.suggested_by = "{}[inhook]".format(self.hook.name)
        event.group = self.hook.group  # set owner
        event.save()
        return JsonResponse({"status": "ok"})
