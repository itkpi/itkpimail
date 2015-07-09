# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0039_suggestedevent_suggested_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suggestedevent',
            name='date',
            field=models.DateTimeField(verbose_name='Submitted', auto_now_add=True),
        ),
    ]
