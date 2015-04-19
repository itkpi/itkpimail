from django import forms
from events.mailchimp_utils import list_list


class CampaignCreateForm1(forms.Form):
    subscribers_list = forms.ChoiceField(label='List', choices=list_list)


class CampaignCreateForm2(CampaignCreateForm1):
    subject = forms.CharField(label='Subject')
