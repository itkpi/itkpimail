from django.conf.urls import include, url
from django.views.generic import TemplateView, RedirectView
from events.admin import SuggestedEventAdmin
from events.views import PreviewView, PreviewView1, PreviewView2, CompaniesListView, CompanyView, SuggestPublicView, \
    JSONEventsView

urlpatterns = [
    url(r'^company/(?P<tenant_slug>[^/]*)$', CompanyView.as_view(), name="company"),
    url(r'^companies$', CompaniesListView.as_view(), name="companies_list"),
    url(r'^company/(?P<slug>[^/]*)/suggest$', SuggestPublicView.as_view(), name="suggest_event_old"),
    url(r'^company/(?P<slug>[^/]*)/suggest/thanks$', TemplateView.as_view(template_name='companies/suggest_thanks.html'),
        name="suggest_thanks_old"),

    url(r'^preview/(?P<p_id>\d*)$', PreviewView.as_view(), name="preview"),
    url(r'^preview/(?P<p_id>\d*)/step1$', PreviewView1.as_view(), name="preview_step1"),
    url(r'^preview/(?P<p_id>\d*)/step2$', PreviewView2.as_view(), name="preview_step2"),

    # tenant-based pages
    url(r'^$', CompanyView.as_view(), name="event_list"),
    url(r'^calendar$', TemplateView.as_view(template_name='companies/calendar.html'), name="calendar"),
    url(r'^events.json$', JSONEventsView.as_view(), name="calendar"),
    url(r'^suggest$', SuggestPublicView.as_view(), name="suggest_event"),
    url(r'^suggest/thanks$', TemplateView.as_view(template_name='companies/suggest_thanks.html'), name="suggest_thanks"),
]
