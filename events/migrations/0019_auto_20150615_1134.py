# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0018_auto_20150524_0851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='image_url',
            field=models.CharField(max_length=200, default=''),
        ),
        migrations.AlterField(
            model_name='event',
            name='level',
            field=models.CharField(max_length=10, choices=[('NONE', 'none'), ('TRAINEE', 'trainee'), ('JUNIOR', 'junior'), ('MIDDLE', 'middle')], default='NONE'),
        ),
        migrations.AlterField(
            model_name='event',
            name='registration',
            field=models.CharField(max_length=200, default=''),
        ),
        migrations.AlterField(
            model_name='event',
            name='social',
            field=redactor.fields.RedactorField(verbose_name='Social'),
        ),
    ]
