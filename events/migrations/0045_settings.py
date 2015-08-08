# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import events.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('events', '0044_auto_20150806_1549'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('is_default', events.fields.ExclusiveBooleanFieldOnOwnerGroups(default=True, verbose_name='Selected', help_text='Only one settings configuration can be selected at one time.')),
                ('event_suggest_callback', models.URLField()),
                ('group', models.ForeignKey(null=True, verbose_name='Owner group', to='auth.Group', editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
