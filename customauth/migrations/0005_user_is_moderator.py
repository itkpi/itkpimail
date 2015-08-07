# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customauth', '0004_tenant_big_logo_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_moderator',
            field=models.BooleanField(default=False, help_text='Designates whether the user can edit without opening admin site.', verbose_name='moderator user status'),
        ),
    ]
