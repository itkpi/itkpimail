from itkpimail import settings
import mailchimp

mailchimp_api = mailchimp.Mailchimp(settings.MAILCHIMP_API_KEY)


def list_list():
    return [(item['id'], item['name']) for item in mailchimp_api.lists.list()['data']]


def get_list(list_id):
    return mailchimp_api.lists.list(filters=[{'list_id': list_id}])['data'][0]
