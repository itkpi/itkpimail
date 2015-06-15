# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0021_auto_20150615_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='owner',
            field=models.ForeignKey(editable=False, null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='preview',
            name='owner',
            field=models.ForeignKey(editable=False, null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='template',
            name='owner',
            field=models.ForeignKey(editable=False, null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='template',
            name='slug',
            field=models.CharField(default='unknown.html', max_length=80),
        ),
        migrations.AlterUniqueTogether(
            name='template',
            unique_together=set([('slug', 'owner')]),
        ),
    ]
