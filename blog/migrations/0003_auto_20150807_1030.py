# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blogentry_published'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogentry',
            options={'verbose_name': 'Blog post'},
        ),
    ]
