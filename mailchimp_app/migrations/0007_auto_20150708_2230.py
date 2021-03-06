# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('mailchimp_app', '0006_auto_20150708_2226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailchimpcredential',
            name='owner',
            field=models.ForeignKey(editable=False, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
