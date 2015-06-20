from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView


urlpatterns = [
    # Examples:
    url(r'^$', RedirectView.as_view(url='/admin/')),
    url(r'^events/', include('events.urls')),

    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/', include(admin.site.urls)),

    url(r'^redactor/', include('redactor.urls')),
]
