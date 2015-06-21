# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0023_auto_20150615_1502'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='special',
            field=models.BooleanField(default=False),
        ),
    ]
