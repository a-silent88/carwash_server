from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from . import views 

urlpatterns = [
    url(r'^services\/(?P<suburl>add)/$', views.ServiceView.as_view(), name='services_add'),
    url(r'^services\/(?P<suburl>edit)\/(?P<pk>\d+)', views.ServiceView.as_view(), name='services_edit'),
    url(r'^services\/(?P<suburl>del)\/(?P<pk>\d+)', views.ServiceView.as_view(), name='services_del'),
    url(r'^services/$', views.ServiceView.as_view(), name='services'),
]