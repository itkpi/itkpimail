# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20150424_0840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='variables',
            field=models.CharField(blank=True, null=True, max_length=200, default='', help_text='"~!~"-separated variables list'),
        ),
    ]
