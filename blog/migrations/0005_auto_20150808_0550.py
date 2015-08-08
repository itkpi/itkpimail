# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20150807_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogentry',
            name='published',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]
