# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0035_auto_20150708_2230'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='publish',
            field=models.BooleanField(default=False, help_text="This event will be published on your company's page"),
        ),
    ]
