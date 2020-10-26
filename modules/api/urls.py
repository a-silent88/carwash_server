from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets
from . import views

admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'terminal', views.TerminalList)
router.register(r'sessions', views.SessionList)
urlpatterns = [
    url(r'^api\/', include(router.urls)),
    url(r'^api\/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api_sessions/add_user/', views.AddUser.as_view()),
    url(r'^api_sessions/add_card/', views.AddCard.as_view()),
    url(r'^api_sessions/delete_user/', views.DelUser.as_view()),
    url(r'^api_sessions/get_pays/', views.GetPays.as_view()),
    url(r'^api_sessions/', views.SessionApi.as_view()),
]
