from django.conf.urls import include, url

from signup.source import source_list, source_create, source_update, source_delete, source_all, source_lock
from views import default, signup, delete, jobs, email_list, download_csv, eald_csv
from view_email_autocomplete import EmailAutocomplete, UserAutocomplete
from registration import register, user
from django.contrib.auth.views import login
from signup.auth import JanesForm

urlpatterns = [
    url(r'email-autocomplete/$', UserAutocomplete.as_view(), name='email-autocomplete'),
    url(r'^$', default, name='default'),
    url(r'^jobs/(?P<title>[a-zA-Z0-9\-_ .]+)$', jobs, name='jobs'),
    url(r'^signup/(?P<pk>\d+)$', signup, name='signup'),
    url(r'^delete/(?P<pk>\d+)$', delete, name='delete'),
    url(r'^source/$', source_list, name='source_list'),
    url(r'^source/cr$', source_create, name='source_create'),
    url(r'^source/u/(?P<pk>[a-zA-Z0-9\-_ .]+)$', source_update, name='source_update'),
    url(r'^source/d/(?P<pk>[a-zA-Z0-9\-_ .]+)$', source_delete, name='source_delete'),
    url(r'^source/a$', source_all, name='source_all'),
    url(r'^sourcelock/$', source_lock, name='source_lock'),
    url(r'^register/$', register, name='register'),
    url(r'^user/$', user, name='user'),
    url(r'^email/(?P<role>[a-zA-Z0-9\-_ .]+)$', email_list, name='email_list'),
    url(r'^csv/$', download_csv, name='download_csv'),
    url(r'^eald/$', eald_csv, name='eald_csv'),
    # override the login form. 
    url(r'^login/$', login, {'authentication_form': JanesForm}, name='login'),
    url('^', include('django.contrib.auth.urls')),
]
