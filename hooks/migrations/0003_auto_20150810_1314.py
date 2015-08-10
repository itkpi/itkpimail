# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hooks', '0002_auto_20150810_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hook',
            name='event',
            field=models.CharField(max_length=50, choices=[('event_suggested', 'Event suggested'), ('blog_post_published', 'Blog post published'), ('blog_post_published_personal', 'Personal blog post published')]),
        ),
    ]
