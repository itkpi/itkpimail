from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse


urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/suggest/')),

    url(r'^events/', include('events.urls')),
    url(r'^suggest/', include('suggest.urls')),

    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/', include(admin.site.urls)),

    url(r'^redactor/', include('redactor.urls')),
]
