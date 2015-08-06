from customauth.admin import CustomGroup
from customauth.models import Tenant
from customauth.utils import get_tenant
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import FormView, View, TemplateView, ListView
from events.forms import CampaignCreateForm1, CampaignCreateForm2, SuggestForm, SuggestPublicForm
from events.mailchimp_utils import get_mailchimp_api, get_list
from events.models import Preview, Event
from events.admin import fill_suggested_by


class PreviewView(View):
    def get(self, request, p_id):
        preview = Preview.objects.get(pk=int(p_id))
        return HttpResponse(preview.body)


class PreviewView1(FormView):
    form_class = CampaignCreateForm1
    template_name = 'preview.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.preview_id = int(kwargs['p_id'])
        self.model = Preview.objects.get(pk=self.preview_id)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.model.list_id = form.cleaned_data['list_id']
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

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.preview_id = int(kwargs['p_id'])
        self.model = Preview.objects.get(pk=self.preview_id)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        options = {
            'list_id': form.cleaned_data['list_id'],
            'subject': form.cleaned_data['subject'],
            'from_name': form.cleaned_data['from_name'],
            'from_email': form.cleaned_data['from_email'],
            }

        content = {
            'html': self.model.body,
        }

        data = get_mailchimp_api().campaigns.create('regular', options, content)

        self.model.published = True
        self.model.mailchimp_url = "https://admin.mailchimp.com/campaigns/wizard/html-paste?id={}".\
                                   format(data['web_id'])
        self.model.save()
        return redirect(self.model.mailchimp_url, permanent=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        preview = Preview.objects.get(pk=self.preview_id)
        context['preview'] = preview
        return context

    def get_initial(self):
        list_info = get_list(self.model.list_id)
        initial = {
            'subject': list_info['default_subject'],
            'from_name': list_info['default_from_name'],
            'from_email': list_info['default_from_email'],
        }
        initial.update(self.model.__dict__)
        return initial


class CompaniesListView(TemplateView):
    template_name = 'companies/list.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['companies'] = Tenant.objects.all().order_by('slug')
        return data


class CompanyView(ListView):
    template_name = 'companies/home.html'
    model = Event
    paginate_by = 5

    def get_queryset(self):
        return Event.objects.filter(owner__groups=self.tenant.group, publish=True).\
            order_by('-when')

    def dispatch(self, request, *args, **kwargs):
        self.tenant = get_tenant(kwargs, request)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tenant'] = self.tenant
        return data


class SuggestPublicView(FormView):
    form_class = SuggestPublicForm
    template_name = 'companies/suggest_public.html'

    def dispatch(self, request, *args, **kwargs):
        self.tenant = get_tenant(kwargs, request)
        self.user = request.user
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        object = form.save(commit=False)
        object.group = self.tenant.group
        fill_suggested_by(object, self.user)
        object.save()
        return redirect('suggest_thanks')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tenant'] = self.tenant
        return data


class SuggestView(FormView):
    form_class = SuggestForm
    template_name = 'companies/suggest.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.preview_id = int(kwargs['p_id'])
        self.model = Preview.objects.get(pk=self.preview_id)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.model.list_id = form.cleaned_data['list_id']
        self.model.save()
        return redirect('preview_step2', self.preview_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        preview = Preview.objects.get(pk=self.preview_id)
        context['preview'] = preview
        return context
