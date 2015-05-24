# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def move_speaker_to_agenda(apps, schema_editor):
    Event = apps.get_model("events", "Event")
    for event in Event.objects.all():
        event.agenda = """<p><strong>Програма:</strong></p>
                          %s
                          <strong>Спікери:</strong></p>
                          <p>%s</p>""" % (event.agenda, event.speaker)
        event.save()


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0016_auto_20150524_0836'),
    ]

    operations = [
        migrations.RunPython(move_speaker_to_agenda),
        migrations.RemoveField(
            model_name='event',
            name='speaker',
        ),
    ]
