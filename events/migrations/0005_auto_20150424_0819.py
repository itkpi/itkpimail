# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_template_variables'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=redactor.fields.RedactorField(verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='template',
            name='variables',
            field=models.CharField(default='', max_length=200, null=True, help_text='"~!~"-separated variables list'),
        ),
    ]
