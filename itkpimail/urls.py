from django.utils.translation import ugettext_lazy as _
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView

admin.site.site_header = _("IT KPI Maillist Generation Engine")
admin.site.site_title = _("IT KPI Maillist Generation Engine")
admin.site.index_title = _("IT KPI Maillist Generation Engine")

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/events/', permanent=False)),
    url(r'^events/', include('events.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^redactor/', include('redactor.urls')),

    url(r'^admin_tools/', include('admin_tools.urls')),
]
