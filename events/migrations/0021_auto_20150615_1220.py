# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User

from django.db import models, migrations
from django.conf import settings


def set_preview_to_itkpi(apps, schema_editor):
    Preview = apps.get_model("events", "Preview")
    for preview in Preview.objects.all():
        if preview.owner == None:
            preview.owner_id = User.objects.get(pk=1).id
            preview.save()


def set_template_to_itkpi(apps, schema_editor):
    Template = apps.get_model("events", "Template")
    for template in Template.objects.all():
        if template.owner == None:
            user = User.objects.get(pk=1)
            template.owner_id = user.id
            template.save()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0020_event_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='preview',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.RunPython(set_preview_to_itkpi),
        migrations.AddField(
            model_name='template',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.RunPython(set_template_to_itkpi),
    ]
