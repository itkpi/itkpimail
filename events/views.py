import datetime
from customauth.models import Tenant
from customauth.utils import get_tenant
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import FormView, View, TemplateView, ListView, DetailView
from events.eventsmonkey import EventsMonkey
from events.forms import CampaignCreateForm1, CampaignCreateForm2, SuggestForm, SuggestPublicForm, SuggestEditPublicForm
from events.mailchimp_utils import get_mailchimp_api, get_list
from events.models import Preview, Event, SuggestedEvent
from events.admin import fill_suggested_by
from hooks.models import EVENT_SUGGESTED, EVENT_SUGGESTED_CHANGED
from hooks.views import call_hook


class PreviewView(View):
    def get(self, request, p_id):
        preview = Preview.objects.get(pk=int(p_id))
        return HttpResponse(preview.body)


class PreviewView1(FormView):
    form_class = CampaignCreateForm1
    template_name = 'preview.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        self.preview_id = int(kwargs['p_id'])
        self.model = Preview.objects.get(pk=self.preview_id)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.model.list_id = form.cleaned_data['list_id']
        self.model.owner = self.user
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
        self.user = request.user
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
        self.model.owner = self.user
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


class EventView(DetailView):
    template_name = 'companies/one_event.html'
    model = Event


class JSONEventsView(View):
    def get(self, request):
        start = datetime.date.fromtimestamp(int(request.GET['start']))
        end = datetime.date.fromtimestamp(int(request.GET['end']))
        events = Event.objects.filter(when__gte=start, when__lt=end)
        return JsonResponse({'events': [event.to_dict() for event in events]})


class JSONEventView(DetailView):
    model = Event

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(
            self.get_object().to_dict(),
            **response_kwargs
        )


class SuggestPublicView(FormView):
    form_class = SuggestPublicForm
    template_name = 'companies/suggest_public.html'

    def dispatch(self, request, *args, **kwargs):
        self.tenant = get_tenant(kwargs, request)
        self.user = request.user
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        data = form.cleaned_data
        if not data['registration_url']:
            data['registration_url'] = None
        data['team'] = settings.EVENTSMONKEY_TEAM
        api = EventsMonkey(settings.EVENTSMONKEY_URL)
        suggested = api.suggest(data)
        return redirect('suggested_edit', suggested['secret'])

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tenant'] = self.tenant
        return data


class SuggestEditPublicView(FormView):
    form_class = SuggestEditPublicForm
    template_name = 'companies/suggested_edit_public.html'

    def dispatch(self, request, *args, **kwargs):
        self.tenant = get_tenant(kwargs, request)
        self.user = request.user
        self.secret = kwargs['secret']
        self.api = EventsMonkey(settings.EVENTSMONKEY_URL)
        self.event_data = self.api.get(self.secret)
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial.update(self.event_data)
        return initial

    def form_valid(self, form):
        data = form.cleaned_data
        if not data['registration_url']:
            data['registration_url'] = None
        data['team'] = settings.EVENTSMONKEY_TEAM
        api = EventsMonkey(settings.EVENTSMONKEY_URL)
        suggested = api.edit(self.secret, data)
        return redirect('suggested_edit', suggested['secret'])

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tenant'] = self.tenant
        data['edit_url'] = self.request.\
            build_absolute_uri(reverse('suggested_edit', args=(self.secret,)))
        data['secret'] = self.secret
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


@receiver(post_save, sender=SuggestedEvent)
def event_suggestion_signal(sender, instance, created, **kwargs):
    if created:
        call_hook(EVENT_SUGGESTED, instance)
    else:
        call_hook(EVENT_SUGGESTED_CHANGED, instance)
