# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20150424_0819'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='agenda',
            field=redactor.fields.RedactorField(default='', verbose_name='Agenda'),
        ),
        migrations.AddField(
            model_name='event',
            name='place',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='speaker',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='event',
            name='when',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=redactor.fields.RedactorField(verbose_name='Comment'),
        ),
    ]
