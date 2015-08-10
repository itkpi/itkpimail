# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0047_settings_event_suggest_callback_body'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='settings',
            name='group',
        ),
        migrations.DeleteModel(
            name='Settings',
        ),
    ]
