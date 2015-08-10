# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hook',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('event', models.CharField(choices=[('event_suggest', 'Event suggestion'), ('blog_post_publish', 'Blog post published')], max_length=10)),
                ('url', models.URLField()),
                ('method', models.CharField(choices=[('GET', 'GET'), ('POST', 'POST')], max_length=10)),
                ('body', models.TextField(help_text="Template for POST request. You can use variable 'object'.")),
                ('group', models.ForeignKey(editable=False, to='auth.Group', verbose_name='Owner group', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
