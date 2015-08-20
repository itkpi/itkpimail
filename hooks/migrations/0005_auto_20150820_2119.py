# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hooks', '0004_incominghook'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incominghook',
            name='key',
            field=models.CharField(max_length=50),
        ),
    ]
