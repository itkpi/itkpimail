from django.core.urlresolvers import reverse
from django.test import TestCase

# Create your tests here.
class AccountTest(TestCase):
    def test_home_accessible(self):
        self.assertEqual(self.client.get(reverse('home_page')).status_code, 200)