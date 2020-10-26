from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url, include
from . import views

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    # path('/', views.MainView.as_view(), name='index'),
    url(r'^reports/$', views.ReportsView.as_view(), name='reports'),
    url(r'^settings/$', views.Setting.as_view(), name='settings'),
]