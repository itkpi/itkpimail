from django.views.generic.base import TemplateView
from django.conf.urls import include, url
from suggest.views import SuggestView


urlpatterns = [
    url(r'^$', SuggestView.as_view(), name="suggest_main"),
    url(r'^thanks/$', TemplateView.as_view(template_name='thanks.html'), name="suggest_thanks")
]
