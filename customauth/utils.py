from customauth.models import Tenant, User
from django.db import models
from django.http import Http404


def get_tenant(kwargs, request):
    if 'tenant_slug' in kwargs:
        return Tenant.objects.get(slug=kwargs['tenant_slug'])
    elif request.tenant:
        return request.tenant
    else:
        raise Http404("Tenant not found")
