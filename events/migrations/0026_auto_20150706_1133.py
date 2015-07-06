# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0025_auto_20150628_1820'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='published',
            field=models.CharField(max_length=200, default=None, null=True, editable=False),
        ),
        migrations.AlterField(
            model_name='event',
            name='special',
            field=models.BooleanField(default=False, help_text='This event will be published in special way (if template supports it). You can set special on "promoted" events or some events you wish to draw attention to.'),
        ),
    ]
