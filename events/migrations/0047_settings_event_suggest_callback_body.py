# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0046_auto_20150808_0600'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='event_suggest_callback_body',
            field=models.TextField(help_text="For POST request. You can use variable 'object' which issuggested event", default=''),
            preserve_default=False,
        ),
    ]
