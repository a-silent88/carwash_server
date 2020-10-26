from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader, loader_tags
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.base import View
from django.contrib.auth.models import User
#from django.utils.functional import curry
from django.contrib import messages
from django.db import models
from django.core.paginator import Paginator
from django.db.models import Q

class MainView(View):
    def get(self, request):
        return render(request, 'main.html')

class ReportsView(View):
    def get(self, request):
        return render(request, 'reports.html')

class Setting(View):
    def get(self, request):
        return render(request, 'setting.html')