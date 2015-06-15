from django.shortcuts import render, render_to_response
from django.views.generic import FormView
from suggest.forms import SuggestEventForm


class SuggestView(FormView):
    form_class = SuggestEventForm
    template_name = 'suggest.html'

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('suggest_thanks')
