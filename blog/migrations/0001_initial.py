# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=256)),
                ('slug', models.CharField(max_length=50)),
                ('content', models.TextField()),
                ('tags', models.TextField()),
                ('date_published', models.DateField()),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
