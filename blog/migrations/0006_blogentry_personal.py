# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20150808_0550'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogentry',
            name='personal',
            field=models.BooleanField(default=True),
        ),
    ]
