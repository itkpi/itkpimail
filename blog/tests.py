from blog.models import BlogEntry
from customauth.models import User
from customauth.tests import UserTestMixin, TenantTestMixin
from django.contrib.auth.models import Permission
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.timezone import now

class BlogTestCase(TestCase):
    def create_blog_post(self, owner, name='random_post', published=True, personal=False, tags='tag'):
        entry = BlogEntry(title=name,
                          slug=name,
                          content='{} content'.format(name),
                          tags=tags,
                          published=published,
                          personal=personal,
                          date_published=now(),
                          owner=owner)
        entry.save()
        return entry


class BlogTest(UserTestMixin, BlogTestCase):
    def test_published(self):
        entry = self.create_blog_post(owner=self.user, published=True)
        r = self.client.get(reverse('blog_feed'))
        self.assertContains(r, entry.title)

    def test_unpublished(self):
        entry = self.create_blog_post(owner=self.user, published=False)
        r = self.client.get(reverse('blog_feed'))
        self.assertNotContains(r, entry.title)


class BlogSecurityTest(TenantTestMixin, BlogTestCase):
    """
    Own/Foreign post: covered
    User has permission or no: covered
    Personal: not covered
    Published: not covered
    Staff / not staff: not covered
    """
    def post_dict(self, post):
        new_data = post.__dict__
        new_data['title'] = 'new_title'
        return new_data

    def assertPostUpdateNotAllowed(self, post):
        new_data = self.post_dict(post)
        editor_url = reverse('blog_post_editor', args=(post.pk,))
        response = self.client.post(editor_url, new_data)
        # self.assertRedirects(response, '/accounts/login/?next={}'.format(editor_url))
        self.assertEqual(response.status_code, 403)

    def assertPostUpdateAllowed(self, post):
        new_data = self.post_dict(post)
        response = self.client.post(reverse('blog_post_editor', args=(post.pk,)), new_data)
        self.assertEqual(response.status_code, 200)

    def test_edit_foreign_personal_post(self):
        post_owner = self.create_user('user1')

        user = self.create_user('user2')
        permission = Permission.objects.get(codename='change_blogentry')
        user.user_permissions.add(permission)
        self.login(user)

        post = self.create_blog_post(owner=post_owner, personal=True, published=True)
        self.assertPostUpdateNotAllowed(post)

    def test_edit_foreign_company_post(self):
        post_owner = self.create_user('user1')
        permission = Permission.objects.get(codename='change_blogentry')
        post_owner.user_permissions.add(permission)

        user = self.create_user('user2')
        self.login(user)

        post = self.create_blog_post(owner=post_owner, personal=False, published=True)
        self.assertPostUpdateNotAllowed(post)

    def test_edit_own_post(self):
        post_owner = self.create_user('user1')
        permission = Permission.objects.get(codename='change_blogentry')
        post_owner.user_permissions.add(permission)
        self.login(post_owner)

        post = self.create_blog_post(owner=post_owner, personal=True, published=True)
        self.assertPostUpdateAllowed(post)

    def test_edit_no_permission_to_edit(self):
        post_owner = self.create_user('user1')
        self.login(post_owner)

        post = self.create_blog_post(owner=post_owner, personal=True, published=True)
        self.assertPostUpdateNotAllowed(post)

    def test_staff_edit_foreign_personal_post(self):
        post_owner = self.create_user('user1')

        user = self.create_user('user2')
        permission = Permission.objects.get(codename='change_blogentry')
        user.user_permissions.add(permission)
        user.is_staff = True
        user.save()
        self.login(user)

        post = self.create_blog_post(owner=post_owner, personal=True, published=True)
        self.assertPostUpdateAllowed(post)

    def test_staff_edit_foreign_company_post(self):
        post_owner = self.create_user('user1')

        user = self.create_user('user2')
        permission = Permission.objects.get(codename='change_blogentry')
        user.user_permissions.add(permission)
        user.is_staff = True
        user.save()
        self.login(user)

        post = self.create_blog_post(owner=post_owner, personal=False, published=True)
        self.assertPostUpdateAllowed(post)

    def test_view_own_personal_unpublished_post(self):
        post_owner = self.create_user('user1')
        self.login(post_owner)

        post = self.create_blog_post(owner=post_owner, personal=True, published=False)
        response = self.client.get(reverse('blog_post', args=(post.slug,)))
        self.assertEqual(response.status_code, 200)

    def test_view_own_company_unpublished_post(self):
        post_owner = self.create_user('user1')
        self.login(post_owner)

        post = self.create_blog_post(owner=post_owner, personal=False, published=False)
        response = self.client.get(reverse('blog_post', args=(post.slug,)))
        self.assertEqual(response.status_code, 200)

    def test_view_foreign_personal_unpublished_post(self):
        post_owner = self.create_user('user1')

        user = self.create_user('user2')
        self.login(user)

        post = self.create_blog_post(owner=post_owner, personal=True, published=False)
        response = self.client.get(reverse('blog_post', args=(post.slug,)))
        self.assertEqual(response.status_code, 403)

    def test_view_foreign_company_unpublished_post(self):
        post_owner = self.create_user('user1')

        user = self.create_user('user2')
        self.login(user)

        post = self.create_blog_post(owner=post_owner, personal=False, published=False)
        response = self.client.get(reverse('blog_post', args=(post.slug,)))
        self.assertEqual(response.status_code, 403)

    def test_staff_view_foreign_personal_unpublished_post(self):
        post_owner = self.create_user('user1')

        user = self.create_user('user2')
        user.is_staff = True
        user.save()
        self.login(user)

        post = self.create_blog_post(owner=post_owner, personal=True, published=False)
        response = self.client.get(reverse('blog_post', args=(post.slug,)))
        self.assertEqual(response.status_code, 403)

    def test_staff_view_foreign_company_unpublished_post(self):
        post_owner = self.create_user('user1')

        user = self.create_user('user2')
        user.is_staff = True
        user.save()
        self.login(user)

        post = self.create_blog_post(owner=post_owner, personal=False, published=False)
        response = self.client.get(reverse('blog_post', args=(post.slug,)))
        self.assertEqual(response.status_code, 200)

    def test_view_own_company_published_post(self):
        post_owner = self.create_user('user1')
        post_owner.is_staff = True
        post_owner.save()
        self.login(post_owner)

        post = self.create_blog_post(owner=post_owner, personal=False, published=True)
        response = self.client.get(reverse('blog_post', args=(post.slug,)))
        self.assertEqual(response.status_code, 200)

    def test_staff_view_foreign_company_published_post(self):
        post_owner = self.create_user('user1')

        user = self.create_user('user2')
        user.is_staff = True
        user.save()
        self.login(user)

        post = self.create_blog_post(owner=post_owner, personal=False, published=True)
        response = self.client.get(reverse('blog_post', args=(post.slug,)))
        self.assertEqual(response.status_code, 200)

    def test_staff_move_to_company(self):
        post_owner = self.create_user('user1')
        post_owner.is_staff = True
        post_owner.save()
        self.login(post_owner)

        post = self.create_blog_post(owner=post_owner, personal=True, published=True)
        response = self.client.get(reverse('blog_post_to_company', args=(post.pk,)))
        self.assertIn(response.status_code, [200, 302])

    def test_move_to_company(self):
        post_owner = self.create_user('user1')
        self.login(post_owner)

        post = self.create_blog_post(owner=post_owner, personal=True, published=True)
        response = self.client.get(reverse('blog_post_to_company', args=(post.pk,)))
        self.assertEqual(response.status_code, 403)

    def test_staff_move_to_personal(self):
        post_owner = self.create_user('user1')
        post_owner.is_staff = True
        post_owner.save()
        self.login(post_owner)

        post = self.create_blog_post(owner=post_owner, personal=False, published=True)
        response = self.client.get(reverse('blog_post_to_personal', args=(post.pk,)))
        self.assertIn(response.status_code, [200, 302])

    def test_move_to_personal(self):
        post_owner = self.create_user('user1')
        self.login(post_owner)

        post = self.create_blog_post(owner=post_owner, personal=False, published=True)
        response = self.client.get(reverse('blog_post_to_personal', args=(post.pk,)))
        self.assertEqual(response.status_code, 403)
