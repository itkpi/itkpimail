# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User

from django.db import models, migrations
from django.conf import settings


def set_owner_to_itkpi(apps, schema_editor):
    Event = apps.get_model("events", "Event")
    for event in Event.objects.all():
        if event.owner == None:
            event.owner_id = User.objects.get(pk=1).id
            event.save()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0019_auto_20150615_1134'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='owner',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.RunPython(set_owner_to_itkpi),
    ]
