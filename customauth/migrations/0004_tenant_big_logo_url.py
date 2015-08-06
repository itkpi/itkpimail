# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customauth', '0003_tenant'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenant',
            name='big_logo_url',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
