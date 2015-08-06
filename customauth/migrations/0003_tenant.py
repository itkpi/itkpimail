# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customauth', '0002_customgroup'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('slug', models.CharField(max_length=50, help_text='Short name')),
                ('domain', models.CharField(max_length=256)),
                ('group', models.ForeignKey(to='customauth.CustomGroup')),
            ],
        ),
    ]
