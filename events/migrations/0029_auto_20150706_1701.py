# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0028_gitremote'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gitremote',
            options={'verbose_name': 'Github remote'},
        ),
        migrations.AlterUniqueTogether(
            name='gitremote',
            unique_together=set([('remote', 'owner')]),
        ),
    ]
