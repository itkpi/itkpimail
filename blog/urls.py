from blog.views import BlogListView
from django.conf.urls import include, url
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^$', BlogListView.as_view(), name="blog_article_list"),
    url(r'^post/(?P<slug>.*)$', BlogListView.as_view(), name="blog_post"),
]
