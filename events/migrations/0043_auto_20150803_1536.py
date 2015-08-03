# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0042_auto_20150803_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='social',
            field=redactor.fields.RedactorField(help_text='How to get to the event, useful links and comments', verbose_name='Social'),
        ),
        migrations.AlterField(
            model_name='suggestedevent',
            name='social',
            field=redactor.fields.RedactorField(help_text='How to get to the event, useful links and comments', verbose_name='Social'),
        ),
    ]
