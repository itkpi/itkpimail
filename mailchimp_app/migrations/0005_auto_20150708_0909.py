# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mailchimp_app', '0004_auto_20150615_1549'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mailchimpcredential',
            options={'verbose_name': 'Mailchimp API Key'},
        ),
    ]
