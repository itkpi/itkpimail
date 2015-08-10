from django.contrib import admin
from hooks.models import Hook


class HookAdmin(admin.ModelAdmin):
    list_display = ('event', 'url', 'method')

    def save_model(self, request, obj, form, change):
        obj.group = request.tenant.group
        obj.save()

admin.site.register(Hook, HookAdmin)
