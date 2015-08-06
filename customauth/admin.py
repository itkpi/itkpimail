from customauth.models import User, CustomGroup, Tenant
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from events.admin import filter_by_owner_group_admin
from events.middlewares import get_current_request


class CustomUserCreationForm(UserCreationForm):
    def save(self, commit=True):
        user = super().save(commit)
        if commit:
            user.save()
            request = get_current_request()
            if not request.user.is_supreme:  # supreme user can choose group after creation
                for group in request.user.groups.all():
                    user.groups.add(group)
                user.save()

        return user


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'is_supreme',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_supreme:
            return self.readonly_fields + ('is_supreme', 'groups')
        return self.readonly_fields

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_supreme:
            return queryset.filter(groups=request.user.groups.all())
        return queryset

admin.site.register(User, CustomUserAdmin)


class CustomGroupAdmin(GroupAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_supreme:
            q = Q()
            for group in request.user.groups.all():
                q |= Q(name=group.name)
            return queryset.filter(q)
        return queryset

admin.site.register(CustomGroup, CustomGroupAdmin)


class TenantAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'group', 'domain')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_supreme:
            queryset = queryset.filter(group=request.user.groups.all())
        return queryset

admin.site.register(Tenant, TenantAdmin)
