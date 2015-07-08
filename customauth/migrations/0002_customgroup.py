# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('customauth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomGroup',
            fields=[
            ],
            options={
                'verbose_name': 'Group',
                'proxy': True,
            },
            bases=('auth.group',),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
    ]
