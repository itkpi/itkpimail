# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_template_is_default'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='image_url',
            field=models.CharField(max_length=200, default=''),
        ),
    ]
