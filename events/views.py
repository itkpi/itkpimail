from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from events.forms import CampaignCreateForm1, CampaignCreateForm2
from events.models import Preview


class PreviewView(FormView):
    form_class = CampaignCreateForm1
    template_name = 'preview.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.preview_id = int(kwargs['p_id'])
        self.model = Preview.objects.get(pk=self.preview_id)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Post.objects.create(**form.cleaned_data)
        print(form.cleaned_data)
        self.model.list_id = form.cleaned_data['subscribers_list']
        self.model.save()
        return redirect('preview_step2', self.preview_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        preview = Preview.objects.get(pk=self.preview_id)
        context['preview'] = preview
        return context


class PreviewView2(FormView):
    form_class = CampaignCreateForm2
    template_name = 'preview.html'
    success_url = '/success/'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.preview_id = int(kwargs['p_id'])
        self.model = Preview.objects.get(pk=self.preview_id)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Post.objects.create(**form.cleaned_data)
        print(form.cleaned_data)
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        preview = Preview.objects.get(pk=self.preview_id)
        context['preview'] = preview
        return context

    def get_initial(self):
        return {'subscribers_list': self.model.list_id}
