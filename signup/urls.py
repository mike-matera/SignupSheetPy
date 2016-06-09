from django.conf.urls import url

from signup.source import source_list, source_create, source_update, source_delete, source_all
from views import default, signup, delete, jobs

urlpatterns = [
    url(r'^$', default, name='default'),
    url(r'^jobs/(?P<title>[a-zA-Z0-9\-_ ]+)$', jobs, name='jobs'),
    url(r'^signup/(?P<pk>\d+)$', signup, name='signup'),
    url(r'^delete/(?P<pk>\d+)$', delete, name='delete'),
    url(r'^source/$', source_list, name='source_list'),
    url(r'^source/cr$', source_create, name='source_create'),
    url(r'^source/u/(?P<pk>[a-zA-Z0-9\-_ ]+)$', source_update, name='source_update'),
    url(r'^source/d/(?P<pk>[a-zA-Z0-9\-_ ]+)$', source_delete, name='source_delete'),
    url(r'^source/a$', source_all, name='source_all'),
]
