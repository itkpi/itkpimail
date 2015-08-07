from blog.forms import BlogPostForm
from blog.models import BlogEntry
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, UpdateView


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
