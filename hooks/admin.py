from uuid import uuid4
from django.contrib import admin
from django import forms
from hooks.models import Hook, IncomingHook


class HookAdmin(admin.ModelAdmin):
    list_display = ('event', 'url', 'method')

    def save_model(self, request, obj, form, change):
        obj.group = request.tenant.group
        obj.save()

admin.site.register(Hook, HookAdmin)


class CreateIncomingHookForm(forms.ModelForm):
    class Meta:
        model = IncomingHook
        exclude = ['key']


class IncomingHookAdmin(admin.ModelAdmin):
    list_display = ('event', 'name')
    add_form = CreateIncomingHookForm

    def save_model(self, request, obj, form, change):
        if not change:
            obj.key = str(uuid4()).replace('-', '')
            obj.save()

    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)

admin.site.register(IncomingHook, IncomingHookAdmin)
