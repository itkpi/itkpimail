from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView

admin.site.site_header = "IT KPI Maillist Generation Engine"
admin.site.site_title = "IT KPI Maillist Generation Engine"
admin.site.index_title = "IT KPI Maillist Generation Engine"

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/admin/', permanent=False)),
    url(r'^events/', include('events.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^redactor/', include('redactor.urls')),

    url(r'^admin_tools/', include('admin_tools.urls')),
]
