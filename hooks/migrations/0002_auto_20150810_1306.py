# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hooks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hook',
            name='event',
            field=models.CharField(choices=[('event_suggested', 'Event suggested'), ('blog_post_published', 'Blog post published'), ('blog_post_published_personal', 'Personal blog post published')], max_length=10),
        ),
    ]
