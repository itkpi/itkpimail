# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_auto_20150424_1038'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='registration',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='event',
            name='when_end',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='when_end_time',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='when_time',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='level',
            field=models.CharField(choices=[('TRAINEE', 'trainee'), ('JUNIOR', 'junior'), ('MIDDLE', 'middle')], max_length=10, default='TRAINEE'),
        ),
        migrations.AlterField(
            model_name='event',
            name='when',
            field=models.DateField(null=True),
        ),
    ]
