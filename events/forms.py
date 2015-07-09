from django import forms
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from events.mailchimp_utils import list_list


class CampaignCreateForm1(forms.Form):
    list_id = forms.ChoiceField(label=_('Subscription List'), choices=list_list)


class SuggestForm(forms.Form):
    group = forms.ModelChoiceField(label=_('Suggest to group'), queryset=Group.objects.all())
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)

class CampaignCreateForm2(CampaignCreateForm1):
    subject = forms.CharField()
    from_name = forms.CharField()
    from_email = forms.CharField()
