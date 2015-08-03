from django.conf.urls import include, url
from django.views.generic import TemplateView
from events.admin import SuggestedEventAdmin
from events.views import PreviewView, PreviewView1, PreviewView2, CompaniesListView, CompanyView, SuggestPublicView

urlpatterns = [
    url(r'^company/(?P<slug>[^/]*)$', CompanyView.as_view(), name="company"),
    url(r'^companies$', CompaniesListView.as_view(), name="companies_list"),
    url(r'^company/(?P<slug>[^/]*)/suggest$', SuggestPublicView.as_view(), name="suggest_event"),
    url(r'^company/(?P<slug>[^/]*)/suggest/thanks$', TemplateView.as_view(template_name='companies/suggest_thanks.html'),
        name="suggest_thanks"),

    url(r'^preview/(?P<p_id>\d*)$', PreviewView.as_view(), name="preview"),
    url(r'^preview/(?P<p_id>\d*)/step1$', PreviewView1.as_view(), name="preview_step1"),
    url(r'^preview/(?P<p_id>\d*)/step2$', PreviewView2.as_view(), name="preview_step2"),
]
