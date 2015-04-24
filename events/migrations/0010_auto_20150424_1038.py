# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_event_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='image_url',
            field=models.CharField(max_length=200, blank=True, default=''),
        ),
    ]
