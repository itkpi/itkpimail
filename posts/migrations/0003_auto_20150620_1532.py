# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20150620_1337'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vkcredential',
            options={'verbose_name': 'VK Credential'},
        ),
    ]
