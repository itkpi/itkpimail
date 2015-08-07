# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customauth', '0005_user_is_moderator'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_moderator',
        ),
    ]
