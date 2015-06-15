from django import forms


class SuggestEventForm(forms.Form):
    from_email = forms.CharField()
