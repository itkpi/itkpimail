from accounts.views import HomeView, AccountView, AccountEditView
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'accounts/login.html'},
        name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'template_name': 'accounts/logged_out.html'},
        name='logout'),
    url(r'^change_password/$', 'django.contrib.auth.views.password_change',
        {'template_name': 'accounts/password_change_form.html'},
        name='password_change'),
    url(r'^change_password/done/$', 'django.contrib.auth.views.password_change_done',
        {'template_name': 'accounts/password_change_done.html'},
        name='password_change_done'),

    url(r'^home/$', HomeView.as_view(), name='home_page'),
    url(r'^profile/$', AccountView.as_view(), name='account'),
    url(r'^profile/edit/$', AccountEditView.as_view(), name='account_edit'),
)
