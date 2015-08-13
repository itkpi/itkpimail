import logging
from django.template import Template, Context
from hooks.models import Hook
import requests

logger = logging.getLogger(__name__)


def call_hook(event_name, instance):
    for hook in Hook.objects.filter(event=event_name):
        logger.debug("Hook called: making {} request to {}".format(hook.method, hook.url))
        if hook.method == 'POST':
            data = Template(hook.body).render(Context({'object': instance}))
            requests.post(hook.url, data.encode('utf-8'))
        else:
            requests.request(hook.method, hook.url)
