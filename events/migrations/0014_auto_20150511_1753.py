# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_event_when_time_required'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='registration',
            field=models.CharField(blank=True, max_length=200, default=''),
        ),
    ]
