from django.template import Template, Context
from hooks.models import Hook
import requests


def call_hook(event_name, instance):
    for hook in Hook.objects.filter(event=event_name):
        if hook.method == 'POST':
            data = Template(hook.body).render(Context({'object': instance}))
            requests.post(hook.url, data.encode('utf-8'))
        else:
            requests.request(hook.method, hook.url)
