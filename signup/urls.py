from django.urls import path, include

from signup.views import views
from signup.views.views import download_csv, eald_csv, jobs, email_list, signup_view, delete
from signup.views.source import source_list, source_create, source_update, source_delete, source_all, source_lock
from signup.views.registration import user, register
from signup.views.react import react_jobs

urlpatterns = [
    path('source/', source_list, name='source_list'),
    path('source/cr', source_create, name='source_create'),
    path('source/u/<pk>', source_update, name='source_update'),
    path('source/d/<pk>', source_delete, name='source_delete'),
    path('source/a', source_all, name='source_all'),
    path('sourcelock/', source_lock, name='source_lock'),

    path('user/', user, name='user'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', register, name='register'),

    path('csv/', download_csv, name='download_csv'),
    path('eald/', eald_csv, name='eald_csv'),

    path('jobs/<title>/', jobs, name='jobs'),
    path('email/<role>/', email_list, name='email_list'),
    path('signup/<pk>', signup_view, name='signup'),
    path('delete/<pk>', delete, name='delete'),

    path('r/jobs/<title>/', react_jobs, name='react_jobs'),

    path('', views.index, name='index'),
]
