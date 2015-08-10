from django.contrib.auth.models import Group
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from events.middlewares import get_current_request


class User(AbstractUser):
    class Meta:
        db_table = 'auth_user'
        verbose_name = 'User'

    is_supreme = models.BooleanField(_('supreme user status'), default=False,
        help_text=_('Designates whether the user can ignore ownership of items.'))


class CustomGroup(Group):
    class Meta:
        proxy = True
        verbose_name = _('Group')


class Tenant(models.Model):
    slug = models.CharField(max_length=50, help_text=_("Short name"))
    domain = models.CharField(max_length=256)
    group = models.ForeignKey(CustomGroup)
    big_logo_url = models.CharField(max_length=256, null=True)


# Abstract models to support multi-tenant models. Model can be either be owned by specific user or by group
# TODO: check ownership by Tenant, not Group

class OwnedModelManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        if get_current_request().user.is_anonymous() or not get_current_request().user.is_supreme:
            queryset = queryset.filter(owner__groups=get_current_request().tenant.group)
        return queryset


class OwnedModel(models.Model):
    class Meta:
        abstract = True
    owner = models.ForeignKey(User, null=True, editable=False)
    objects = OwnedModelManager()


class GroupOwnedModelManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        if get_current_request().user.is_anonymous() or not get_current_request().user.is_supreme:
            queryset = queryset.filter(group=get_current_request().tenant.group)
        return queryset


class GroupOwnedModel(models.Model):
    class Meta:
        abstract = True
    group = models.ForeignKey(Group, null=True, editable=False, verbose_name=_("Owner group"))
    objects = GroupOwnedModelManager()
