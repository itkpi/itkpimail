from django.contrib import admin
from django.conf.urls import patterns, url

from events.admin import filter_by_owner_group_admin
from posts.models import VKApp, VKCredential, Post, VKGroup
from posts.views import VKAuthView, publish_to_vk


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
                                   self.admin_site.admin_view(VKAuthView.as_view()),
                                   name='posts_vkcredential_add',
                               ),
                           )
        return urls + my_urls

admin.site.register(VKCredential, VKCredentialAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('short_content', 'id', 'owner_groups')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return filter_by_owner_group_admin(queryset, request)

    def owner_groups(self, obj):
        if obj.owner:
            return ','.join(group.name for group in obj.owner.groups.all())

    def short_content(self, obj):
        return obj.plain_content()[:40]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = patterns('',
                           url(
                               r'publish_to_vk/(?P<model_id>.*)$',
                               self.admin_site.admin_view(publish_to_vk),
                               name='post_publish_to_vk',
                           ),
                           )
        return urls + my_urls
admin.site.register(Post, PostAdmin)


class VKGroupAdmin(admin.ModelAdmin):
    list_display = ('group_id', 'is_default', 'owner_groups')

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

    def content(self, obj):
        if obj.content:
            return obj.content[:50] + "..."


admin.site.register(VKGroup, VKGroupAdmin)
