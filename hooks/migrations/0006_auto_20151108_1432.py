# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hooks', '0005_auto_20150820_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hook',
            name='event',
            field=models.CharField(choices=[('event_suggested', 'Event suggested'), ('event_suggested_changed', 'Suggested event changed'), ('blog_post_published', 'Blog post published'), ('blog_post_published_personal', 'Personal blog post published')], max_length=50),
        ),
    ]
