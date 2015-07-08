# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0034_auto_20150708_2226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='owner',
            field=models.ForeignKey(verbose_name='Created by', editable=False, null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='gitremote',
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
    ]
