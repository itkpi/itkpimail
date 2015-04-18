# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='level',
            field=models.CharField(choices=[('NOOB', 'noob'), ('PADAWAN', 'padawan'), ('JEDI', 'jedi')], default='NOOB', max_length=10),
        ),
    ]
