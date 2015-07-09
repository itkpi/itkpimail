from django.utils.translation import ugettext_lazy as _
from itkpimail import settings
from events.middlewares import get_current_request
from mailchimp_app.models import MailChimpCredential

import mailchimp


def get_mailchimp_key(request):
    return MailChimpCredential.objects.\
        get(is_default=True, owner__groups__in=request.user.groups.all()).api_key


def is_mailchimp_configured(request):
    try:
        get_mailchimp_key(request)
        return True
    except MailChimpCredential.DoesNotExist:
        return False


def get_mailchimp_api():
    request = get_current_request()
    try:
        default_key = get_mailchimp_key(request)
    except MailChimpCredential.DoesNotExist:
        raise Exception(_("Check if your API key present."))
    return mailchimp.Mailchimp(default_key)


def list_list():
    lst = get_mailchimp_api().lists.list()
    return [(item['id'], item['name']) for item in lst['data']]


def get_list(list_id):
    return get_mailchimp_api().lists.list(filters=[{'list_id': list_id}])['data'][0]
