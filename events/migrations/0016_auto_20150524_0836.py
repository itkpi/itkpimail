# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_auto_20150524_0758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='agenda',
            field=redactor.fields.RedactorField(default='\n                                <strong>Програма:</strong><br/>\n                                <ul>\n                                <li></li>\n                                </ul>\n                                <strong>Спікери:</strong><br/>\n                                <ul>\n                                <li>&nbsp;</li>\n                                </ul>\n                                ', verbose_name='Agenda'),
        ),
    ]
