from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig

class MailChimpAppConfig(AppConfig):
    name = 'mailchimp_app'
    verbose_name = _('MailChimp Configuration')
