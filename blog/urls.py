from blog.views import BlogListView, BlogPostView, BlogPostEditView, BlogListUnpublishedView
from django.conf.urls import include, url
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^$', BlogListView.as_view(), name="blog_article_list"),
    url(r'^unpublished$', BlogListUnpublishedView.as_view(), name="blog_unpublished_article_list"),
    url(r'^post/(?P<slug>[^\/]*)$', BlogPostView.as_view(), name="blog_post"),
    url(r'^post/(?P<pk>\d+)/edit$', BlogPostEditView.as_view(), name="blog_post_editor"),
]
