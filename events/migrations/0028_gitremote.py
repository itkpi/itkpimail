# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import events.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0027_auto_20150706_1204'),
    ]

    operations = [
        migrations.CreateModel(
            name='GitRemote',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('remote', models.CharField(max_length=200)),
                ('is_default', events.fields.ExclusiveBooleanFieldOnOwnerGroups(default=True, help_text='If any of remotes is selected, it will be used. Otherwise, Templates from DB will be used.', verbose_name='Selected')),
                ('owner', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, editable=False)),
            ],
        ),
    ]
