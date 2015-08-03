# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0040_auto_20150709_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='place',
            field=models.CharField(max_length=200, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='suggestedevent',
            name='place',
            field=models.CharField(max_length=200, blank=True, null=True),
        ),
    ]
