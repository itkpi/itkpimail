# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20150807_1030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogentry',
            name='tags',
            field=models.CharField(max_length=256),
        ),
    ]
