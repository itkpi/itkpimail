from customauth.models import Tenant


class TenantsMiddleware(object):
    def process_request(self, request):
        tenant_search = Tenant.objects.filter(domain=request.get_host())
        request.tenant = None
        if tenant_search.exists():
            request.tenant = tenant_search.get()
