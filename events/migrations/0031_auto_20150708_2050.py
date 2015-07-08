# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0030_auto_20150708_0909'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'permissions': (('ignore_tenancy', 'Can see items owned by any tenant'),)},
        ),
    ]
