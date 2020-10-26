from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from . import views 

urlpatterns = [
    url(r'^(?P<url>pays)\/(?P<suburl>add)', views.PayView.as_view(), name='add_comment'),
    url(r'^pays/$', views.PayView.as_view(), name='pays'),
]