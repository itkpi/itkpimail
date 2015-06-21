from django.contrib import admin
from django.contrib.admin.helpers import ActionForm
from django import forms
from django.forms import ModelForm

from events.middlewares import get_current_request
from events.adminactions import generate_mail, preview
from events.models import Event, Template, Preview, filter_by_owner_group
from itkpimail import settings
from redactor.widgets import RedactorEditor


def filter_by_owner_group_admin(queryset, request):
    if not request.user.is_superuser:
        queryset = filter_by_owner_group(queryset, request)
    return queryset


# Previews


class PreviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'template', 'owner_groups')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return filter_by_owner_group_admin(queryset, request)

    def owner_groups(self, obj):
        if obj.owner:
            return ','.join(group.name for group in obj.owner.groups.all())

admin.site.register(Preview, PreviewAdmin)

# Events


class EventActionForm(ActionForm):
    template = forms.ModelChoiceField(queryset=Template.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        request = get_current_request()

        default_template = list(Template.objects.filter(is_default=True, owner__groups__in=request.user.groups.all()))
        if default_template:
            kwargs["initial"] = {"template": default_template[0].id}

        super().__init__(*args, **kwargs)

        self.fields['template'].queryset = Template.objects.filter(owner__groups__in=request.user.groups.all())


class EventAdminForm(ModelForm):
    class Media:
        css = {
            'all': (
                '%sevents/css/redactor-custom.css' % settings.STATIC_URL,
            )
        }

    social = forms.CharField(widget=RedactorEditor, required=False)

    def clean(self):
        cleaned_data = super().clean()
        when_time = cleaned_data['when_time']
        when_time_required = cleaned_data['when_time_required']
        if when_time_required and not when_time:
            raise forms.ValidationError("when_time field is required!")
        if not when_time_required and when_time:
            raise forms.ValidationError("when_time field is required to be empty!")

    def clean_level(self):
        level = self.cleaned_data['level']
        if level == 'NONE':
            raise forms.ValidationError("This field is required")
        return level


class EventAdmin(admin.ModelAdmin):
    action_form = EventActionForm
    actions = [generate_mail, preview]
    ordering = ['-when']

    form = EventAdminForm

    fields = ('title', 'special', 'agenda', 'image_url', 'level', 'place',
              ('when', 'when_time', 'when_time_required'), ('when_end', 'when_end_time'), 'registration', 'social')
    list_display = ('title', 'when', 'level', 'owner_groups')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return filter_by_owner_group_admin(queryset, request)

    def owner_groups(self, obj):
        if obj.owner:
            return ','.join(group.name for group in obj.owner.groups.all())


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
    list_display = ('slug', 'is_default', 'owner_groups')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()

    def owner_groups(self, obj):
        if obj.owner:
            return ','.join(group.name for group in obj.owner.groups.all())

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return filter_by_owner_group_admin(queryset, request)

admin.site.register(Template, TemplatesAdmin)
