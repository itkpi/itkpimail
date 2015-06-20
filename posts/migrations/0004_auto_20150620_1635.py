# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import redactor.fields
import events.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0003_auto_20150620_1532'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('content', redactor.fields.RedactorField()),
                ('owner', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VKGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('group_id', models.CharField(max_length=200)),
                ('is_default', events.fields.ExclusiveBooleanFieldOnOwnerGroups(default=True, verbose_name='Selected')),
                ('owner', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, editable=False)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='vk_group',
            field=models.ForeignKey(null=True, to='posts.VKGroup'),
        ),
    ]
