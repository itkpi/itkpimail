from django.contrib import admin

from events.admin import filter_by_owner_group_admin
from mailchimp_app.models import MailChimpCredential


# Register your models here.
class MailChimpCredentialAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_default', 'owner_groups')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return filter_by_owner_group_admin(queryset, request)

    def owner_groups(self, obj):
        if obj.owner:
            return ','.join(group.name for group in obj.owner.groups.all())
admin.site.register(MailChimpCredential, MailChimpCredentialAdmin)
