# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_auto_20150511_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='when_end',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='when_end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='when_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
