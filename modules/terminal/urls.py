from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from . import views 

urlpatterns = [
    url(r'^terminals\/(?P<suburl>add)/$', views.TerminalView.as_view(), name='terminal_add'),
    url(r'^terminals\/(?P<suburl>edit)\/(?P<pk>\d+)', views.TerminalView.as_view(), name='terminal_edit'),
    url(r'^terminals\/(?P<suburl>del)\/(?P<pk>\d+)', views.TerminalView.as_view(), name='terminal_del'),
    url(r'^terminals/$', views.TerminalView.as_view(), name='terminals'),

    url(r'^sessions\/(?P<suburl>add)/$', views.SessionView.as_view(), name='sessions_add'),
    url(r'^sessions\/(?P<suburl>edit)\/(?P<pk>\d+)', views.SessionView.as_view(), name='sessions_edit'),
    url(r'^sessions\/(?P<suburl>del)\/(?P<pk>\d+)', views.SessionView.as_view(), name='sessions_del'),
    url(r'^sessions/$', views.SessionView.as_view(), name='sessions'),
    url(r'^sessions_all/$', views.SessionViewAll.as_view(), name='sessions_all'),
]