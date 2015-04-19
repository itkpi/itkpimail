# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_preview_list_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='template',
            name='variables',
            field=models.CharField(default='', max_length=200, help_text='comma-separated variables list'),
        ),
    ]
