# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mailchimp_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mailchimpcredential',
            options={'verbose_name': 'API Key'},
        ),
        migrations.AlterField(
            model_name='mailchimpcredential',
            name='name',
            field=models.CharField(editable=False, max_length=200, default='default'),
        ),
        migrations.AlterUniqueTogether(
            name='mailchimpcredential',
            unique_together=set([('name', 'owner')]),
        ),
    ]
