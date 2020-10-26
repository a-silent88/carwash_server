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
import modules
# from index import urls 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')), 
    path('', include('modules.api.urls')), 
    path('', include('modules.profiles.urls')),
    path('', include('modules.authentication.urls')),
    path('', include('modules.service.urls')),
    path('', include('modules.terminal.urls')),
    path('', include('modules.paysystem.urls')),
    path('', include('modules.comment.urls')),    
    path('', include('modules.client.urls')), 
    path('', include('modules.history.urls')),                     
]