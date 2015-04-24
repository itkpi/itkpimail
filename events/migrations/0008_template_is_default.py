# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import exclusivebooleanfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_auto_20150424_0848'),
    ]

    operations = [
        migrations.AddField(
            model_name='template',
            name='is_default',
            field=exclusivebooleanfield.fields.ExclusiveBooleanField(default=False),
        ),
    ]
