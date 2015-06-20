# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VKCredential',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('access_token', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'VK API Key',
            },
        ),
        migrations.AlterModelOptions(
            name='vkapp',
            options={'verbose_name': 'VK Application'},
        ),
        migrations.AddField(
            model_name='vkcredential',
            name='app',
            field=models.ForeignKey(to='posts.VKApp'),
        ),
        migrations.AddField(
            model_name='vkcredential',
            name='owner',
            field=models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='vkcredential',
            unique_together=set([('owner', 'app')]),
        ),
    ]
