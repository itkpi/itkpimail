from blog.views import BlogListView, BlogPostView, BlogPostEditView, BlogListUnpublishedView, BlogPostCreateView, \
    BlogPostPublishView, BlogPostUnpublishView
from django.conf.urls import url


urlpatterns = [
    url(r'^$', BlogListView.as_view(), name="blog_article_list"),
    url(r'^unpublished$', BlogListUnpublishedView.as_view(), name="blog_unpublished_article_list"),
    url(r'^post/(?P<slug>[^\/]*)$', BlogPostView.as_view(), name="blog_post"),
    url(r'^write$', BlogPostCreateView.as_view(), name="blog_create_post"),
    url(r'^post/(?P<pk>\d+)/edit$', BlogPostEditView.as_view(), name="blog_post_editor"),
    url(r'^post/(?P<pk>\d+)/publish$', BlogPostPublishView.as_view(), name="blog_post_publish"),
    url(r'^post/(?P<pk>\d+)/unpublish$', BlogPostUnpublishView.as_view(), name="blog_post_unpublish"),

    # url(r'^author/(?P<username>[^\/]*)$', AuthorView.as_view(), name="author"),
]
