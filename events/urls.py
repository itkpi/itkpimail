from django.conf.urls import include, url
from events.views import PreviewView

urlpatterns = [
    url(r'^preview/(?P<p_id>\d*)$', PreviewView.as_view(), name="preview"),
]

