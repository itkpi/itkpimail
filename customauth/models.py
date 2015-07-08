from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class CustomUser(AbstractUser):
    class Meta:
        db_table = 'auth_user'
        verbose_name = 'User'

    is_supreme = models.BooleanField(_('supreme user status'), default=False,
        help_text=_('Designates whether the user can ignore ownership of items.'))
