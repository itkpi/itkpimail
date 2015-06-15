# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import events.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mailchimp_app', '0003_auto_20150615_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailchimpcredential',
            name='is_default',
            field=events.fields.ExclusiveBooleanFieldOnOwnerGroups(verbose_name='Selected', default=True),
        ),
    ]
