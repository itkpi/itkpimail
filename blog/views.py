import datetime
from blog.forms import BlogPostForm, BlogPostFormCreate
from blog.models import BlogEntry
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, UpdateView, CreateView, View
from django.views.generic.detail import SingleObjectMixin


class BlogListView(ListView):
    template_name = 'blog/list.html'
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
        return BlogEntry.objects.filter(published=False).\
            order_by('-date_published')

    @method_decorator(login_required(login_url='/admin/login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class BlogPostView(DetailView):
    template_name = 'blog/post.html'
    model = BlogEntry


class BlogPostEditView(UpdateView):
    form_class = BlogPostForm
    template_name = 'blog/editor.html'
    model = BlogEntry

    @method_decorator(login_required(login_url='/admin/login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class BlogPostCreateView(CreateView):
    form_class = BlogPostFormCreate
    template_name = 'blog/editor.html'
    model = BlogEntry

    def form_valid(self, form):
        form.instance.owner = self.user
        return super().form_valid(form)

    @method_decorator(login_required(login_url='/admin/login'))
    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        return super().dispatch(request, *args, **kwargs)


class BlogPostPublishView(SingleObjectMixin, View):
    model = BlogEntry

    @method_decorator(login_required(login_url='/admin/login'))
    def get(self, request, **kwargs):
        self.object = self.get_object()
        self.object.published = True
        self.object.save()
        return HttpResponseRedirect(reverse('blog_article_list'))


class BlogPostUnpublishView(SingleObjectMixin, View):
    model = BlogEntry

    @method_decorator(login_required(login_url='/admin/login'))
    def get(self, request, **kwargs):
        self.object = self.get_object()
        self.object.published = False
        self.object.save()
        return HttpResponseRedirect(reverse('blog_unpublished_article_list'))
