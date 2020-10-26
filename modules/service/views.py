from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.db import models
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Service
from .form import ServiceForm

# Create your views here.
class ServiceView(View):
    def get(self, request, suburl='', pk=''):
        if suburl == 'add':
            form = ServiceForm()
            return render(request, 'service_item.html', {'form': form})

        if suburl == 'edit':
            term = Service.objects.get(pk=pk)
            form = ServiceForm(instance=term)
            return render(request,'service_item.html', {'form': form})

        if suburl == 'del':
            Service.objects.get(pk=pk).delete()
            return HttpResponse('Услуга удалина')

        services = Service.objects.all()
        data = {
            'services': services
        }
        return render(request, 'service.html', data)
    
    def post(self, request, suburl='', pk=''):
        if suburl == 'add':
            form = ServiceForm(request.POST)
            if form.is_valid:
                form.save()
                return HttpResponse('Услуга добавленна')
        if suburl == 'edit':
            term = Service.objects.get(pk=pk)
            form = ServiceForm(self.request.POST, instance=term)
            if form.is_valid:
                form.save()
                return HttpResponse('Услуга изменина')