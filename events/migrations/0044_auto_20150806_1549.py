# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0043_auto_20150803_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='when',
            field=models.DateField(null=True, help_text='Event beginning date'),
        ),
        migrations.AlterField(
            model_name='event',
            name='when_end',
            field=models.DateField(blank=True, null=True, help_text='Event ending date'),
        ),
        migrations.AlterField(
            model_name='event',
            name='when_end_time',
            field=models.TimeField(blank=True, null=True, help_text='Event ending time'),
        ),
        migrations.AlterField(
            model_name='event',
            name='when_time',
            field=models.TimeField(blank=True, null=True, help_text='Event beginning time'),
        ),
        migrations.AlterField(
            model_name='suggestedevent',
            name='when',
            field=models.DateField(null=True, help_text='Event beginning date'),
        ),
        migrations.AlterField(
            model_name='suggestedevent',
            name='when_end',
            field=models.DateField(blank=True, null=True, help_text='Event ending date'),
        ),
        migrations.AlterField(
            model_name='suggestedevent',
            name='when_end_time',
            field=models.TimeField(blank=True, null=True, help_text='Event ending time'),
        ),
        migrations.AlterField(
            model_name='suggestedevent',
            name='when_time',
            field=models.TimeField(blank=True, null=True, help_text='Event beginning time'),
        ),
    ]
