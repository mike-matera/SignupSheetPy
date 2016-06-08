from django.conf.urls import url
from views import hello
from signup.source import source_list, source_create, source_update, source_delete

urlpatterns = [
    url(r'^$', hello),
    url(r'^source/$', source_list, name='source_list'),
    url(r'^source/cr$', source_create, name='source_create'),
    url(r'^source/u/(?P<pk>[a-zA-Z0-9\-_ ]+)$', source_update, name='source_update'),
    url(r'^source/d/(?P<pk>[a-zA-Z0-9\-_ ]+)$', source_delete, name='source_delete'),
]
