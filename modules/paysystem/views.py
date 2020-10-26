from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.db import models
from django.core.paginator import Paginator
from django.db.models import Q
from .form import PayFormAdd
from .models import Pay, StatusPay
from modules.profiles.models import CustomUser


class PayView(View):
    def get(self, request, url='', suburl=''):
        return render(request, 'pays.html')

    def post(self, request, url='', suburl=''):
        if suburl == 'add':
            client = request.POST.get('id_client')
            price = request.POST.get('price')
            path = request.POST.get('path')

            pay = Pay.objects.create(
                status = StatusPay.objects.get(pk=1),
                client = CustomUser.objects.get(pk=client),
                price = price
            )
            client = CustomUser.objects.get(pk=client)
            client.balance = int(price) + int(client.balance)
            client.save()
        return redirect(path)