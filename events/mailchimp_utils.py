from itkpimail import settings
import mailchimp

mailchimp_api = mailchimp.Mailchimp(settings.MAILCHIMP_API_KEY)


def create_campaign(list_id, subject):
    mailchimp_api.campaigns.create("regular", {'list_id': list_id, 'subject': subject}, )


def list_list():
    return [(item['id'], item['name']) for item in mailchimp_api.lists.list()['data']]
