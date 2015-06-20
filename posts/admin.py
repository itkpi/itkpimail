from django.contrib import admin
from django.conf.urls import patterns, url

from events.admin import filter_by_owner_group_admin
from posts.models import VKApp, VKCredential
from posts.views import vk_auth_view, vk_auth_done_view, vk_auth_save_view


class VKAppAdmin(admin.ModelAdmin):
    # TODO: refactor all admin models with owner to inherit some base model
    list_display = ('name', 'app_id', 'is_default', 'owner_groups')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return filter_by_owner_group_admin(queryset, request)

    def owner_groups(self, obj):
        if obj.owner:
            return ','.join(group.name for group in obj.owner.groups.all())
admin.site.register(VKApp, VKAppAdmin)


class VKCredentialAdmin(admin.ModelAdmin):
    list_display = ('owner', 'app', 'owner_groups')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(owner=request.user)
        return queryset

    def owner_groups(self, obj):
        if obj.owner:
            return ','.join(group.name for group in obj.owner.groups.all())

    def get_urls(self):
        urls = super().get_urls()
        my_urls = patterns('',
                           url(
                               r'do_auth',
                               self.admin_site.admin_view(vk_auth_view),
                               name='posts_vkcredential_add',
                           ),
                           url(
                               r'auth_done',
                               self.admin_site.admin_view(vk_auth_done_view),
                               name='posts_vkcredential_auth_done',
                           ),
                           url(
                               r'add/(?P<access_token>.*)$',
                               self.admin_site.admin_view(vk_auth_save_view),
                               name='posts_vkcredential_auth_save',
                           ),
                           )
        return urls + my_urls

admin.site.register(VKCredential, VKCredentialAdmin)
