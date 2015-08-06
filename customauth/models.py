from django.contrib.auth.models import Group
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


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
