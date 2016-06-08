from django.conf.urls import url
from views import hello
from skipper import source_list, source_create, source_update, source_delete

urlpatterns = [
    url(r'^$', hello),
    url(r'^skipper/$', source_list, name='source_list'),
    url(r'^skipper/cr$', source_create, name='source_create'),
    url(r'^skipper/u/(?P<pk>[a-zA-Z0-9\-_ ]+)$', source_update, name='source_update'),
    url(r'^skipper/d/(?P<pk>[a-zA-Z0-9\-_ ]+)$', source_delete, name='source_delete'),
]
