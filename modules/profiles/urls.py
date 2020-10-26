"""crm_red_eye URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from . import views 

urlpatterns = [
    url(r'^profiles/$', views.profiles_list, name='profiles'),
    url(r'^password/$', views.change_password, name='change_password'),
    url(r'^userchange/$', views.user_change_info, name='user_change_info'),
    url(r'^user\/(?P<user_pk>\d+)', views.user_change_admin, name='user_change_admin'),
    url(r'^user/$', views.user, name='user'),
    url(r'^test_page/$', views.test_page, name='test_page'),
]