# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_blogentry_personal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogentry',
            name='personal',
            field=models.BooleanField(default=True, help_text='If checked, this post will not be shown in thecompany blog, only on personal blog of author'),
        ),
        migrations.AlterField(
            model_name='blogentry',
            name='slug',
            field=models.CharField(max_length=50, help_text='Unique string without special symbols.Will be used in URL of blog post.'),
        ),
    ]
