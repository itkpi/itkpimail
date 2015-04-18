from django.contrib import admin
from django.contrib.admin.helpers import ActionForm
from django import forms
from django.forms import ModelForm
from django.shortcuts import render_to_response
from django.template import Context
from django.template.loader import get_template
from events.models import Event, Template
from itkpimail import settings


class EventActionForm(ActionForm):
    template = forms.ModelChoiceField(queryset=Template.objects.all(), required=False)


def generate_mail(modeladmin, request, queryset):
    template_id = request.POST['template']
    template_slug = Template.objects.get(pk=int(template_id)).slug
    template = get_template(template_slug)
    rendered = template.render(Context({"events": queryset.order_by('date')}))

    return render_to_response("result.html", {"content": str(rendered)})

generate_mail.short_description = "Сгенерировать письмо"


class EventAdmin(admin.ModelAdmin):
    action_form = EventActionForm
    actions = [generate_mail]
    ordering = ['-date']

admin.site.register(Event, EventAdmin)


class TemplateAdminForm(ModelForm):
    class Media:

        css = {
            'all': (
                '%sevents/css/codemirror.css' % settings.STATIC_URL,
            )
        }

        js = (
            '%sevents/js/jquery.min.js' % settings.STATIC_URL,
            '%sevents/js/codemirror.js' % settings.STATIC_URL,
            '%sevents/js/multiplex.js' % settings.STATIC_URL,
            '%sevents/js/xml.js' % settings.STATIC_URL,
            '%sevents/js/javascript.js' % settings.STATIC_URL,
            '%sevents/js/css.js' % settings.STATIC_URL,
            '%sevents/js/htmlmixed.js' % settings.STATIC_URL,
            '%sevents/js/htmlembedded.js' % settings.STATIC_URL,
            '%sevents/js/admin-connector.js' % settings.STATIC_URL,
        )


class TemplatesAdmin(admin.ModelAdmin):

    form = TemplateAdminForm

admin.site.register(Template, TemplatesAdmin)
