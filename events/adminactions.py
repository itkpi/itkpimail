from django import forms
from django.contrib.admin import ACTION_CHECKBOX_NAME
from django.shortcuts import render_to_response, redirect
from django.template import Context, RequestContext
from django.template.loader import get_template
from events.models import Template, Preview


def parse_vars(variables):
    for var in variables:
        if '=' in var:
            name, initial = var.split('=', 2)
            yield {'name': name, 'initial': initial}
        else:
            yield {'name': var, 'initial': None}


def make_template_form(template):
    if not template.variables:
        return
    variables = [var.strip() for var in template.variables.split('~!~')]

    fields = {var['name']: forms.CharField(initial=var['initial']) for var in parse_vars(variables)}
    fields['template'] = forms.CharField(widget=forms.HiddenInput, initial=template.id)
    fields['_selected_action'] = forms.CharField(widget=forms.MultipleHiddenInput)
    return type('TemplateForm', (forms.BaseForm, ), {'base_fields': fields})


def generate_mail(modeladmin, request, queryset):
    template_id = request.POST['template']
    template_db = Template.objects.get(pk=int(template_id))
    TemplateForm = make_template_form(template_db)

    form = None
    if 'apply' in request.POST:
        print(request.POST)
        form = TemplateForm(request.POST)

        if form.is_valid():
            template_slug = template_db.slug
            template = get_template(template_slug)

            variables = form.cleaned_data
            variables['events'] = queryset.order_by('when')
            rendered = template.render(Context(variables))

            preview = Preview(template=template_db, body=str(rendered))
            preview.save()
            return redirect('preview_step1', preview.id)
    if not form:
        form = TemplateForm(initial={'_selected_action': request.POST.getlist(ACTION_CHECKBOX_NAME)})
    return render_to_response('parametrize.html',
                              {'form': form},
                              context_instance=RequestContext(request))

generate_mail.short_description = "Сгенерировать письмо"
