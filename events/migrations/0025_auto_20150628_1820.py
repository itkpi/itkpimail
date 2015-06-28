# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0024_event_special'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created datetime'),
        ),
        migrations.AlterField(
            model_name='event',
            name='owner',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, verbose_name='Created by', editable=False),
        ),
    ]
