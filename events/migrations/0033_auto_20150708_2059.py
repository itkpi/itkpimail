# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0032_auto_20150708_2054'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='template',
            options={'verbose_name_plural': 'Email Templates (Deprecated. Use Github Remote)', 'verbose_name': 'Email Template (Deprecated. Use Github Remote)'},
        ),
    ]
