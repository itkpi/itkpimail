from customauth.models import Tenant, CustomGroup
from django.test import TestCase

class TenantTest(TestCase):
    DOMAIN = 'example.com'

    def test_no_tenant(self):
        self.assertEqual(self.client.get('/').status_code, 403)

    def test_with_tenant(self):
        group = CustomGroup(name='GROUP')
        group.save()
        tenant = Tenant(slug='group', domain=self.DOMAIN, group=group, big_logo_url='logo.jpg')
        tenant.save()
        self.assertNotEqual(self.client.get('/', SERVER_NAME=self.DOMAIN).status_code, 403)
