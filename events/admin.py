from django.contrib import admin
from django.contrib.admin import helpers
from django.contrib.admin.helpers import ActionForm
from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from events.loaders import is_github_remote_enabled, get_github_repo

from events.middlewares import get_current_request
from events.adminactions import generate_mail, preview, publish, unpublish, accept_suggested, suggest
from events.models import Event, Template, Preview, filter_by_owner_group, GitRemote, SuggestedEvent
from itkpimail import settings
from redactor.widgets import RedactorEditor


def filter_by_owner_group_admin(queryset, request):
    if not request.user.is_supreme:
        queryset = filter_by_owner_group(queryset, request)
    return queryset


# Previews


class PreviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner_groups', 'published', 'mailchimp_url')

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


def choice():
    request = get_current_request()
    if is_github_remote_enabled(request):
        return [(file.name, file.name) for file in get_github_repo(request).get_dir_contents('/')
                if file.name.endswith(".html") or file.name.endswith(".template")]
    else:
        request = get_current_request()

        return [(template.id, template.slug) for template in
                Template.objects.filter(owner__groups__in=request.user.groups.all()).all()]


class EventActionForm(ActionForm):
    template = forms.ChoiceField(choices=choice, required=False)

    def __init__(self, *args, **kwargs):
        request = get_current_request()

        if is_github_remote_enabled(request):
            kwargs["initial"] = {"template": "main.html"}
        else:
            default_template = list(Template.objects.filter(is_default=True,
                                                            owner__groups__in=request.user.groups.all()))
            if default_template:
                kwargs["initial"] = {"template": default_template[0].id}

        super().__init__(*args, **kwargs)


class EventAdminForm(ModelForm):
    class Media:
        css = {
            'all': (
                '%sevents/css/redactor-custom.css' % settings.STATIC_URL,
            )
        }

    social = forms.CharField(widget=RedactorEditor, required=False)
    check_when_time_required = True

    def clean(self):
        cleaned_data = super().clean()
        if self.check_when_time_required:
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



class PublishedListFilter(admin.SimpleListFilter):
    title = 'published state'
    parameter_name = 'published'

    def lookups(self, request, model_admin):
        return (
            ('published', 'Published'),
            ('notpublished', 'Not yet published'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'published':
            return queryset.filter(previews__published=True)
        if self.value() == 'notpublished':
            return queryset.exclude(previews__published=True)


class EventAdmin(admin.ModelAdmin):
    action_form = EventActionForm
    actions = [generate_mail, preview, publish, unpublish, suggest]
    ordering = ['-when']

    form = EventAdminForm

    fieldsets = ((_('Basic info'), {'fields': ('title', 'publish', 'agenda')}),
                 (_('Decorations'), {'fields': ('special', 'image_url', 'level')}),
                 (_('Details'), {'fields': ('place', ('when', 'when_time', 'when_time_required'),
                                            ('when_end', 'when_end_time'), 'registration')}),
                 (_('Additional info'), {'fields': ('social', )}),
                 )
    list_display = ('title', 'when', 'owner', 'date', 'owner_groups', 'email_sent')
    list_filter = (PublishedListFilter, 'special', 'level')

    def save_model(self, request, obj, form, change):
        if not obj.owner:
            obj.owner = request.user
        obj.save()

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return filter_by_owner_group_admin(queryset, request)

    def owner_groups(self, obj):
        if obj.owner:
            return ','.join(group.name for group in obj.owner.groups.all())

    def email_sent(self, obj):
      return obj.previews.filter(published=True).count() > 0
    email_sent.boolean = True


admin.site.register(Event, EventAdmin)

class SuggestedEventAdminForm(EventAdminForm):
    check_when_time_required = False
    registration = forms.CharField(required=False)
    image_url = forms.CharField(required=False)
    level = forms.ChoiceField(required=False, choices=Event.LEVEL_OF_EVENT)


class SuggestedEventAdmin(admin.ModelAdmin):
    form = SuggestedEventAdminForm
    actions = [accept_suggested]
    fields = ('title', 'agenda', 'image_url', 'level', 'place',
              ('when', 'when_time'), ('when_end', 'when_end_time'), 'registration', 'social')
    ordering = ['date']
    list_display = ('title', 'when', 'date', 'group', 'suggested_by')

    def save_model(self, request, obj, form, change):
        obj.group = request.user.groups.all()[0]
        obj.save()

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_supreme:
            queryset = queryset.filter(group=request.user.groups.all())
        return queryset



admin.site.register(SuggestedEvent, SuggestedEventAdmin)

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


# Register your models here.
class GitRemoteAdmin(admin.ModelAdmin):
    list_display = ('remote', 'is_default', 'owner_groups')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return filter_by_owner_group_admin(queryset, request)

    def owner_groups(self, obj):
        if obj.owner:
            return ','.join(group.name for group in obj.owner.groups.all())
admin.site.register(GitRemote, GitRemoteAdmin)
