from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class AuthAppConfig(AppConfig):
    name = 'customauth'
    verbose_name = _('Authentication')
