# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_auto_20150511_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='when_time_required',
            field=models.BooleanField(default=False),
        ),
    ]
