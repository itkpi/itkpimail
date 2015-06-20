# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import events.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VKApp',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=200, default='default')),
                ('app_id', models.IntegerField()),
                ('secret', models.CharField(max_length=200)),
                ('is_default', events.fields.ExclusiveBooleanFieldOnOwnerGroups(verbose_name='Selected', default=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, editable=False)),
            ],
            options={
                'verbose_name': 'VK API Key',
            },
        ),
        migrations.AlterUniqueTogether(
            name='vkapp',
            unique_together=set([('name', 'owner')]),
        ),
    ]
