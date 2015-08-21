# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def create_tenant_domains(apps, schema_editor):
    Tenant = apps.get_model("customauth", "Tenant")
    TenantDomain = apps.get_model("customauth", "TenantDomain")
    for tenant in Tenant.objects.all():
        domain = TenantDomain(domain=tenant.domain, tenant=tenant)
        domain.save()


class Migration(migrations.Migration):

    dependencies = [
        ('customauth', '0006_remove_user_is_moderator'),
    ]

    operations = [
        migrations.CreateModel(
            name='TenantDomain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('domain', models.CharField(max_length=256)),
            ],
        ),
        migrations.AddField(
            model_name='tenantdomain',
            name='tenant',
            field=models.ForeignKey(to='customauth.Tenant'),
        ),
        migrations.RunPython(create_tenant_domains),
        migrations.RemoveField(
            model_name='tenant',
            name='domain',
        ),
    ]
