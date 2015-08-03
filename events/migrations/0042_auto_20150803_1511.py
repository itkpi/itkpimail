# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0041_auto_20150803_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='place',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='suggestedevent',
            name='place',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
