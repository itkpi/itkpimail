import json
from django import forms
from django.contrib.admin import ACTION_CHECKBOX_NAME
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.forms import model_to_dict
from django.shortcuts import render_to_response, redirect, render
from django.template import Context, RequestContext
from django.template.debug import DebugVariableNode
from django.template.loader import get_template
from django.template.backends.django import DjangoTemplates
from django.utils.timezone import now
from events.forms import SuggestForm
from events.loaders import is_github_remote_enabled, get_github_repo
from events.middlewares import get_current_request
from events.models import Template, Preview, Event, SuggestedEvent

from collections import OrderedDict


def parse_vars(variables):
    if not variables:
        variables = []
    else:
        variables = [var.strip() for var in variables.split('~!~')]

    for var in variables:
        if '=' in var:
            name, initial = var.split('=', 2)
            yield {'name': name, 'initial': initial}
        else:
            yield {'name': var, 'initial': None}

def make_template_form(template_id):
    template_obj, variables = retrieve_template(template_id)

    fields = OrderedDict()
    for name in sorted(variables.keys()):
        fields[name] = forms.CharField(initial=variables[name])

    fields['template'] = forms.CharField(widget=forms.HiddenInput, initial=template_id)
    fields['_selected_action'] = forms.CharField(widget=forms.MultipleHiddenInput)
    return type('TemplateForm', (forms.BaseForm, ), {'base_fields': fields})


def generate_mail(modeladmin, request, queryset):
    template_id = request.POST['template']
    template_obj, variables = retrieve_template(template_id)
    TemplateForm = make_template_form(template_id)

    form = None
    if 'apply' in request.POST:
        print(request.POST)
        form = TemplateForm(request.POST)

        if form.is_valid():
            variables = form.cleaned_data
            setup_template_variables(queryset, variables)
            rendered = template_obj.render(Context(variables))

            preview = Preview(body=str(rendered), owner=request.user)
            preview.save()

            for event in queryset:
                event.previews.add(preview)
            return redirect('preview_step1', preview.id)
    if not form:
        form = TemplateForm(initial={'_selected_action': request.POST.getlist(ACTION_CHECKBOX_NAME)})
    return render_to_response('parametrize.html',
                              {'form': form},
                              context_instance=RequestContext(request))

generate_mail.short_description = _("Generate email")


def retrieve_template(template_id):
    request = get_current_request()
    if is_github_remote_enabled(request):
        template_slug = template_id
        variables = json.loads(
            get_github_repo(request).get_file_contents('/' + template_slug + '.defaults').decoded_content.decode())
    else:
        template_db = Template.objects.get(pk=int(template_id))
        template_slug = template_db.slug

        variables = {var["name"]: var["initial"] for var in parse_vars(template_db.variables)}

    engine = DjangoTemplates(
            {
                'NAME': 'mail',
                'APP_DIRS': False,
                'DIRS': [],
                'OPTIONS': {
                    'loaders': [
                        'events.loaders.MyLoader',
                    ],
                },
            })
    template = engine.get_template(template_slug)
    return template, variables


def preview(modeladmin, request, queryset):
    template_id = request.POST['template']

    template, variables = retrieve_template(template_id)

    setup_template_variables(queryset, variables)
    rendered = template.render(Context(variables))

    return render_to_response('pre_preview.html',
                              {'body': rendered},
                              context_instance=RequestContext(request))


preview.short_description = _("Event preview")


def setup_template_variables(queryset, variables):
    variables['events'] = queryset.order_by('when')
    variables['special_events'] = queryset.filter(special=True).order_by('when')


def publish(modeladmin, request, queryset):
    for event in queryset:
        event.publish = True
        event.save()


publish.short_description = _("Publish on company's page")

def unpublish(modeladmin, request, queryset):
    for event in queryset:
        event.publish = False
        event.save()


unpublish.short_description = _("Remove from company's page")


def accept_suggested(modeladmin, request, queryset):
    for suggested_event in queryset:
        kwargs = model_to_dict(suggested_event)
        kwargs.pop('id', None)
        kwargs['date'] = now()
        kwargs['owner'] = request.user
        event = Event(**kwargs)
        event.save()
    modeladmin.message_user(request, _("Suggested events accepted."))
    return redirect(reverse('admin:events_event_changelist'))

accept_suggested.short_description = _("Accept suggested event")


def suggest(modeladmin, request, queryset):
    form = None

    if 'apply' in request.POST:
        form = SuggestForm(request.POST)
        if form.is_valid():
            group_name = form.cleaned_data['group']
            group = Group.objects.get(name=group_name)

            for event in queryset:
                kwargs = model_to_dict(event)
                print(kwargs)
                del kwargs['previews']
                s_event = SuggestedEvent(**kwargs)
                s_event.group = group
                user_group = ','.join(group.name for group in request.user.groups.all())
                s_event.suggested_by = "{}::{}".format(user_group, request.user.username)
                s_event.date = now()
                s_event.save()

            modeladmin.message_user(request, _("Events suggested successfully to group {}.").format(group_name))
            return redirect(request.get_full_path())

    if not form:
        form = SuggestForm(initial={'_selected_action': request.POST.getlist(ACTION_CHECKBOX_NAME)})

    return render(request, 'companies/suggest.html', {'object_list': queryset, 'form': form})

suggest.short_description = _("Suggest event")
