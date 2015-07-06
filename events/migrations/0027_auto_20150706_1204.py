# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0026_auto_20150706_1133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='published',
        ),
        migrations.RemoveField(
            model_name='preview',
            name='template',
        ),
        migrations.AddField(
            model_name='event',
            name='previews',
            field=models.ManyToManyField(to='events.Preview'),
        ),
        migrations.AddField(
            model_name='preview',
            name='mailchimp_url',
            field=models.CharField(null=True, blank=True, editable=False, max_length=200),
        ),
        migrations.AddField(
            model_name='preview',
            name='published',
            field=models.BooleanField(default=False),
        ),
    ]
