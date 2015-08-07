from blog.models import BlogEntry
from django.contrib import admin


class BlogEntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_published', 'published')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()

    def owner_groups(self, obj):
        if obj.owner:
            return ','.join(group.name for group in obj.owner.groups.all())
admin.site.register(BlogEntry, BlogEntryAdmin)
