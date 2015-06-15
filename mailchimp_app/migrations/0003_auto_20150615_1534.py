# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import events.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mailchimp_app', '0002_auto_20150615_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailchimpcredential',
            name='is_default',
            field=events.fields.ExclusiveBooleanFieldOnOwnerGroups(default=True),
        ),
        migrations.AlterField(
            model_name='mailchimpcredential',
            name='name',
            field=models.CharField(default='default', max_length=200),
        ),
    ]
