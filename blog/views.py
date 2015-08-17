from blog.forms import BlogPostForm, BlogPostFormCreate
from blog.models import BlogEntry
from customauth.models import User
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, UpdateView, CreateView, View
from django.views.generic.detail import SingleObjectMixin
from hooks.models import POST_PUBLISHED, POST_PUBLISHED_PERSONAL
from hooks.views import call_hook


def staff_required(login_url=None):
    """
    To perform operation staff status is required
    """
    def check_staff(user):
        return user.is_staff
    return user_passes_test(check_staff, login_url=login_url)


class BlogListView(ListView):
    template_name = 'blog/list.html'
    model = BlogEntry
    paginate_by = 5

    def get_queryset(self):
        return BlogEntry.objects.filter(published=True, personal=False).\
            order_by('-date_published')


class BlogFeedView(ListView):
    template_name = 'blog/feed.html'
    model = BlogEntry
    paginate_by = 5

    def get_queryset(self):
        return BlogEntry.objects.filter(published=True).\
            order_by('-date_published')


class BlogListUnpublishedView(ListView):
    template_name = 'blog/list_unpublished.html'
    model = BlogEntry
    paginate_by = 5

    def get_queryset(self):
        return BlogEntry.objects.filter(published=False, personal=False).\
            order_by('-date_published')

    @method_decorator(login_required)
    @method_decorator(staff_required())
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class BlogPostView(DetailView):
    template_name = 'blog/post.html'
    model = BlogEntry


class BlogPostEditView(UpdateView):
    form_class = BlogPostForm
    template_name = 'blog/editor.html'
    model = BlogEntry

    @method_decorator(login_required())
    @method_decorator(permission_required('blog.change_blogentry'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class BlogPostCreateView(CreateView):
    form_class = BlogPostFormCreate
    template_name = 'blog/editor.html'
    model = BlogEntry

    def form_valid(self, form):
        form.instance.owner = self.user
        if not self.user.is_staff:
            form.instance.personal = True
        return super().form_valid(form)

    @method_decorator(login_required)
    @method_decorator(permission_required('blog.add_blogentry'))
    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        return super().dispatch(request, *args, **kwargs)


class BlogPostPublishView(SingleObjectMixin, View):
    model = BlogEntry

    @method_decorator(login_required)
    def get(self, request, **kwargs):
        self.object = self.get_object()
        if not self.object.can_edit():
            raise PermissionDenied()
        self.object.published = True
        self.object.save()
        if self.object.personal:
            call_hook(POST_PUBLISHED_PERSONAL, self.object)
        else:
            call_hook(POST_PUBLISHED, self.object)
        return HttpResponseRedirect(self.object.get_absolute_url())


class BlogPostUnpublishView(SingleObjectMixin, View):
    model = BlogEntry

    @method_decorator(login_required)
    def get(self, request, **kwargs):
        self.object = self.get_object()
        if not self.object.can_edit():
            raise PermissionDenied()
        self.object.published = False
        self.object.save()
        return HttpResponseRedirect(self.object.get_absolute_url())


class BlogPostToPersonalView(SingleObjectMixin, View):
    model = BlogEntry

    @method_decorator(login_required)
    @method_decorator(staff_required())
    def get(self, request, **kwargs):
        self.object = self.get_object()
        self.object.personal = True
        self.object.save()
        return HttpResponseRedirect(self.object.get_absolute_url())


class BlogPostToCompanyView(SingleObjectMixin, View):
    model = BlogEntry

    @method_decorator(login_required)
    @method_decorator(staff_required())
    def get(self, request, **kwargs):
        self.object = self.get_object()
        self.object.personal = False
        self.object.save()
        return HttpResponseRedirect(self.object.get_absolute_url())


class AuthorListView(ListView):
    template_name = 'blog/author/author_list.html'
    model = User

    def get_queryset(self):
        return super().get_queryset().filter(groups=self.request.tenant.group).order_by('first_name')


class AuthorView(DetailView):
    template_name = 'blog/author/author_detail.html'
    model = User

    def get_object(self, queryset=None):
        return self.model.objects.get(username=self.kwargs['username'])

    def get_context_object_name(self, obj):
        return 'author'


class AuthorPostsView(ListView):
    template_name = 'blog/author/author_posts.html'
    model = BlogEntry
    paginate_by = 5
    personal = False
    published = True

    def dispatch(self, request, *args, **kwargs):
        self.author = User.objects.get(username=kwargs['username'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.author
        return context

    def get_queryset(self):

        if not self.published:
            if self.personal:
                # Permissions check: we should not show unpublished personal posts to
                # not authors of their posts.
                # This filter will return results only if author == request.user
                # (previous filter filtered owner by author and this by request.user)
                if self.request.user != self.author:
                    raise PermissionDenied()
            if not self.personal:
                # Permissions check: we should not show unpublished company posts to
                # non-staff users.
                if not self.request.user.is_staff:
                    raise PermissionDenied()
        qs = BlogEntry.objects.filter(published=self.published, owner=self.author,
                                      personal=self.personal). \
            order_by('-date_published')
        return qs


class AuthorUnpublishedView(AuthorPostsView):
    template_name = 'blog/author/author_unpublished.html'
    published = False
