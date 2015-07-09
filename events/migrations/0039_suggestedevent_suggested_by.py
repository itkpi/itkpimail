# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0038_auto_20150709_1040'),
    ]

    operations = [
        migrations.AddField(
            model_name='suggestedevent',
            name='suggested_by',
            field=models.CharField(default='anonymous', editable=False, max_length=200),
        ),
    ]
