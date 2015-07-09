# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0037_auto_20150709_1011'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='suggestedevent',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='suggestedevent',
            name='previews',
        ),
        migrations.AlterField(
            model_name='event',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False, null=True),
        ),
    ]
