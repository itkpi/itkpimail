from customauth.models import Tenant, TenantDomain
from django.core.exceptions import PermissionDenied


class TenantsMiddleware(object):
    def process_request(self, request):
        tenant_domain_search = TenantDomain.objects.filter(domain=request.get_host())
        request.tenant = None
        if tenant_domain_search.exists():
            domain = tenant_domain_search.get()
            request.tenant = domain.tenant
        else:
            raise PermissionDenied("Tenant domain not found")
