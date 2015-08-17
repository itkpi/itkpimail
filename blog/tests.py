from blog.models import BlogEntry
from customauth.tests import UserTestMixin
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.timezone import now


class BlogTest(UserTestMixin, TestCase):
    def test_published(self):
        entry = BlogEntry(title='BlogTitle1',
                          slug='test',
                          content='Article content',
                          tags='tag',
                          published=True,
                          personal=False,
                          date_published=now(),
                          owner=self.user)
        entry.save()
        r = self.client.get(reverse('blog_feed'))
        self.assertContains(r, entry.title)

    def test_unpublished(self):
        entry = BlogEntry(title='BlogTitle1',
                          slug='test',
                          content='Article content',
                          tags='tag',
                          published=False,
                          personal=False,
                          date_published=now(),
                          owner=self.user)
        entry.save()
        r = self.client.get(reverse('blog_feed'))
        self.assertNotContains(r, entry.title)
