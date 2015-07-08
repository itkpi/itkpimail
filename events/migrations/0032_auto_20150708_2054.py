# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0031_auto_20150708_2050'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='template',
            options={'verbose_name_plural': 'Email Templates (Deprecated. Use Github Remote)', 'permissions': (('ignore_tenancy', 'Can see items owned by any tenant'),), 'verbose_name': 'Email Template (Deprecated. Use Github Remote)'},
        ),
    ]
