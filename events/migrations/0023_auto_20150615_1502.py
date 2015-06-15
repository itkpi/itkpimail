# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import events.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0022_auto_20150615_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='is_default',
            field=events.fields.ExclusiveBooleanFieldOnOwnerGroups(default=False),
        ),
    ]
