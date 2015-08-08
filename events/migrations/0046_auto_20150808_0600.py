# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0045_settings'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='settings',
            options={'verbose_name': 'Settings', 'verbose_name_plural': 'Settings'},
        ),
        migrations.AddField(
            model_name='settings',
            name='event_suggest_callback_method',
            field=models.CharField(default='GET', choices=[('GET', 'GET'), ('POST', 'POST')], max_length=10),
            preserve_default=False,
        ),
    ]
