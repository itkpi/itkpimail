# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20150620_1635'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vkgroup',
            options={'verbose_name': 'VK Group / Public'},
        ),
    ]
