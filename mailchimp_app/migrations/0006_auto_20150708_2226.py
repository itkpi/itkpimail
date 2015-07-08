# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('mailchimp_app', '0005_auto_20150708_0909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailchimpcredential',
            name='owner',
            field=models.ForeignKey(to_field='id', null=True, editable=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
