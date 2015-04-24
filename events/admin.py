from django.contrib import admin
from django.contrib.admin.helpers import ActionForm
from django import forms
from django.forms import ModelForm
from events.adminactions import generate_mail, preview
from events.models import Event, Template, Preview
from itkpimail import settings

# Previews


class PreviewAdmin(admin.ModelAdmin):
    pass
admin.site.register(Preview, PreviewAdmin)

# Events


class EventActionForm(ActionForm):
    template = forms.ModelChoiceField(queryset=Template.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        default_template = list(Template.objects.filter(is_default=True))
        if default_template:
            kwargs["initial"] = {"template": default_template[0].id}
        super().__init__(*args, **kwargs)


class EventAdmin(admin.ModelAdmin):
    action_form = EventActionForm
    actions = [generate_mail, preview]
    ordering = ['-date']

    image_url = forms.CharField(required=False)
    description = forms.CharField(required=False)

admin.site.register(Event, EventAdmin)

# Templates


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

    variables = forms.CharField(required=False)


class TemplatesAdmin(admin.ModelAdmin):
    form = TemplateAdminForm

admin.site.register(Template, TemplatesAdmin)
