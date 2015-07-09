# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0006_require_contenttypes_0002'),
        ('events', '0036_event_publish'),
    ]

    operations = [
        migrations.CreateModel(
            name='SuggestedEvent',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=200)),
                ('agenda', redactor.fields.RedactorField(default='\n                                <strong>Програма:</strong><br/>\n                                <ul>\n                                <li></li>\n                                </ul>\n                                <strong>Спікери:</strong><br/>\n                                <ul>\n                                <li>&nbsp;</li>\n                                </ul>\n                                ', verbose_name='Agenda')),
                ('social', redactor.fields.RedactorField(verbose_name='Social')),
                ('image_url', models.CharField(default='', max_length=200)),
                ('level', models.CharField(default='NONE', choices=[('NONE', 'none'), ('TRAINEE', 'trainee'), ('JUNIOR', 'junior'), ('MIDDLE', 'middle')], max_length=10)),
                ('place', models.CharField(null=True, max_length=200)),
                ('when', models.DateField(null=True)),
                ('when_time', models.TimeField(blank=True, null=True)),
                ('when_end', models.DateField(blank=True, null=True)),
                ('when_end_time', models.TimeField(blank=True, null=True)),
                ('when_time_required', models.BooleanField(default=True)),
                ('publish', models.BooleanField(default=False, help_text="This event will be published on your company's page")),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Created datetime')),
                ('registration', models.CharField(default='', max_length=200)),
                ('special', models.BooleanField(default=False, help_text='This event will be published in special way (if template supports it). You can set special on "promoted" events or some events you wish to draw attention to.')),
                ('group', models.ForeignKey(null=True, editable=False, to='auth.Group', verbose_name='Owner group')),
                ('owner', models.ForeignKey(null=True, editable=False, to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('previews', models.ManyToManyField(to='events.Preview')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterModelOptions(
            name='event',
            options={},
        ),
    ]
