from blog.views import BlogListView, BlogPostView, BlogPostEditView, BlogListUnpublishedView, BlogPostCreateView, \
    BlogPostPublishView, BlogPostUnpublishView, AuthorView, AuthorUnpublishedView, AuthorPostsView, \
    BlogPostToPersonalView, BlogPostToCompanyView, AuthorListView, BlogFeedView
from django.conf.urls import url


urlpatterns = [
    url(r'^$', BlogListView.as_view(), name="blog_article_list"),
    url(r'^feed$', BlogFeedView.as_view(), name="blog_feed"),
    url(r'^unpublished$', BlogListUnpublishedView.as_view(), name="blog_unpublished_article_list"),
    url(r'^post/(?P<slug>[^\/]*)$', BlogPostView.as_view(), name="blog_post"),
    url(r'^write$', BlogPostCreateView.as_view(), name="blog_create_post"),
    url(r'^post/(?P<pk>\d+)/edit$', BlogPostEditView.as_view(), name="blog_post_editor"),
    url(r'^post/(?P<pk>\d+)/publish$', BlogPostPublishView.as_view(), name="blog_post_publish"),
    url(r'^post/(?P<pk>\d+)/unpublish$', BlogPostUnpublishView.as_view(), name="blog_post_unpublish"),
    url(r'^post/(?P<pk>\d+)/to_personal$', BlogPostToPersonalView.as_view(), name="blog_post_to_personal"),
    url(r'^post/(?P<pk>\d+)/to_company$', BlogPostToCompanyView.as_view(), name="blog_post_to_company"),

    url(r'^authors/$', AuthorListView.as_view(), name="author_list"),
    url(r'^author/(?P<username>[^\/]*)$', AuthorView.as_view(), name="author"),
    url(r'^author/(?P<username>[^\/]*)/posts$', AuthorPostsView.as_view(), name="author_posts"),
    url(r'^author/(?P<username>[^\/]*)/posts/unpublished$', AuthorUnpublishedView.as_view(),
        name="author_unpublished_posts"),
    url(r'^author/(?P<username>[^\/]*)/posts/personal$', AuthorPostsView.as_view(personal=True),
        name="author_personal_posts"),
    url(r'^author/(?P<username>[^\/]*)/posts/personal/unpublished$', AuthorUnpublishedView.as_view(personal=True),
        name="author_personal_unpublished_posts"),
]
