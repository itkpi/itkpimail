from blog.models import BlogEntry
from django.shortcuts import render
from django.views.generic import ListView


class BlogListView(ListView):
    template_name = 'blog/list.html'
    model = BlogEntry
    paginate_by = 5

    def get_queryset(self):
        return BlogEntry.objects.filter(published=True).\
            order_by('-date_published')

    def dispatch(self, request, *args, **kwargs):
        self.tenant = request.tenant
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tenant'] = self.tenant
        return data
