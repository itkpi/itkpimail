from django.conf.urls import include, url
from events.views import PreviewView, PreviewView1, PreviewView2, CompaniesListView, CompanyView

urlpatterns = [
    url(r'^company/(?P<slug>.*)$', CompanyView.as_view(), name="company"),
    url(r'^companies$', CompaniesListView.as_view(), name="companies_list"),

    url(r'^preview/(?P<p_id>\d*)$', PreviewView.as_view(), name="preview"),
    url(r'^preview/(?P<p_id>\d*)/step1$', PreviewView1.as_view(), name="preview_step1"),
    url(r'^preview/(?P<p_id>\d*)/step2$', PreviewView2.as_view(), name="preview_step2"),
]
