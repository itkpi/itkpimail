from django import forms


class VKAuthForm(forms.Form):
    url = forms.CharField()
