from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.db import models
from django.core.paginator import Paginator
from django.db.models import Q
from modules.profiles.models import CustomUser

# Create your views here.
class ClientView(View):
    def get(self, request):
        clients = CustomUser.objects.all()
        data = {
            'clients': clients,
        }
        return render(request, 'clients.html', data)