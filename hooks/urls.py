from django.conf.urls import url
from hooks.views import IncomingHookView

urlpatterns = [
    url(r'^incoming/(?P<key>[^\/]*)$', IncomingHookView.as_view(), name="incoming_hook"),
]
