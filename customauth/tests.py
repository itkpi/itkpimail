from customauth.models import Tenant, CustomGroup, User
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


class TenantTestMixin:
    TENANT_DOMAIN = 'testserver'

    def setUp(self):
        super().setUp()
        self.group = CustomGroup(name='GROUP')
        self.group.save()
        self.tenant = Tenant(slug='group', domain=self.TENANT_DOMAIN,
                             group=self.group, big_logo_url='logo.jpg')
        self.tenant.save()


class UserTestMixin(TenantTestMixin):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(username='user',
                                             email='user@example.com',
                                             password='1111')
        self.user.groups.add(self.group)
        self.client.login(username='user', password='1111')
