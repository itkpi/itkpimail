# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0029_auto_20150706_1701'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gitremote',
            options={'verbose_name': 'Github remote with Email Templates', 'verbose_name_plural': 'Github remotes with Email Templates'},
        ),
        migrations.AlterModelOptions(
            name='template',
            options={'verbose_name': 'Email Template (Deprecated. Use Github Remote)', 'verbose_name_plural': 'Email Templates (Deprecated. Use Github Remote)'},
        ),
    ]
