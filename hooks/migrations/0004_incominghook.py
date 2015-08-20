# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('hooks', '0003_auto_20150810_1314'),
    ]

    operations = [
        migrations.CreateModel(
            name='IncomingHook',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('event', models.CharField(max_length=50, choices=[('event_suggest', 'Suggest event')])),
                ('name', models.CharField(max_length=50, help_text='Who will use it')),
                ('key', models.CharField(max_length=50, editable=False)),
                ('group', models.ForeignKey(null=True, editable=False, verbose_name='Owner group', to='auth.Group')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
