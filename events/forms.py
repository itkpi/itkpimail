from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Fieldset, Layout, ButtonHolder, Field, Row, Div
from django import forms
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from events.mailchimp_utils import list_list
from events.models import SuggestedEvent, BaseEvent
from redactor.widgets import RedactorEditor


class CampaignCreateForm1(forms.Form):
    list_id = forms.ChoiceField(label=_('Subscription List'), choices=list_list)


class SuggestForm(forms.Form):
    group = forms.ModelChoiceField(label=_('Suggest to group'), queryset=Group.objects.all())
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)


class CampaignCreateForm2(CampaignCreateForm1):
    subject = forms.CharField()
    from_name = forms.CharField()
    from_email = forms.CharField()


class SuggestPublicForm(forms.Form):
    include_submitter = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        fields = [
            Fieldset(
                'Event details',
                'title',
                'agenda',
                'social',
                'place',
                'level',
                'image_url',
                'registration_url',
            ),
            Fieldset(
                'Date and Time',
                Div(
                    Div(Field('when_start', css_class='dateinput'), css_class='col-md-4'),
                    Div(Field('when_end', css_class='dateinput'), css_class='col-md-4'),
                    Div('only_date', css_class='col-md-4'),
                    css_class='row-fluid'
                ),
            ),
        ]
        if self.include_submitter:
            fields += [
                Fieldset(
                    'Submitter',
                    'submitter_email'
                ),
            ]
        else:
            fields += [
                Field('submitter_email', type='hidden'),
            ]
        fields += [
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            )
        ]
        self.helper.layout = Layout(*fields)
        self.helper.form_method = 'post'
        self.helper.form_action = ''

    title = forms.CharField(help_text=_("Title"), required=True)
    agenda = forms.CharField(help_text=_("Agenda"), required=True, widget=RedactorEditor)
    social = forms.CharField(help_text=_("Social"), required=True, widget=RedactorEditor)
    image_url = forms.CharField(help_text=_("Image URL"), required=True,
                                label='Image URL')
    place = forms.CharField(help_text=_("Place"), required=True)
    level = forms.ChoiceField(help_text=_("Level"), required=True,
                              choices=BaseEvent.LEVEL_OF_EVENT)
    when_start = forms.CharField(help_text=_("Date and time of start"), required=True)
    only_date = forms.BooleanField(help_text=_("If checked only date will be printed"), required=False)
    when_end = forms.CharField(help_text=_("Date and time of end"), required=False)
    registration_url = forms.CharField(help_text=_("Registration link"), required=False,
                                       label='Registration URL')
    submitter_email = forms.CharField(help_text=_("Your email"), required=True)


class SuggestEditPublicForm(SuggestPublicForm):
    include_submitter = False
