from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from events.mailchimp_utils import list_list
from events.models import SuggestedEvent


class CampaignCreateForm1(forms.Form):
    list_id = forms.ChoiceField(label=_('Subscription List'), choices=list_list)


class SuggestForm(forms.Form):
    group = forms.ModelChoiceField(label=_('Suggest to group'), queryset=Group.objects.all())
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)


class CampaignCreateForm2(CampaignCreateForm1):
    subject = forms.CharField()
    from_name = forms.CharField()
    from_email = forms.CharField()


class SuggestPublicForm(forms.ModelForm):
    class Meta:
        model = SuggestedEvent
        exclude = ['when_time_required', 'publish', 'special']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.form_action = ''

    registration = forms.CharField(help_text=_("Registration link"), required=False)
    place = forms.CharField(help_text=_("Місце проведення " <a href="https://vk.com/page-42456628_49958531?f=Place">[?]</a></p>), required=False)
