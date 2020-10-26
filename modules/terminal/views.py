from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import render_to_response, get_object_or_404

from django.views.generic.base import View
from django.db import models
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Terminal, Session, StatusTerminal, Status
from .form  import TerminalForm, SessionForm
from threading import Thread
# Create your views here.
import asyncio
import time

def checkIpAddress(ip):
    try:
        accept_ip = Terminal.objects.filter(ipAddress='127.0.0.1').values_list('ipAddress', flat=True)[0]
        if accept_ip == ip:
            return True
    except:
        return False

def ping(host):
    import os
    terminal = Terminal.objects.get(ipAddress=host)
    response = os.system("ping -c 1 " + host)
    
    if response == 0:
        terminal.status = StatusTerminal.objects.get(pk=1)
    else:
        terminal.status = StatusTerminal.objects.get(pk=2)

    terminal.save()

class ThreadCustom(Thread):
    def __init__(self, value):
        """Инициализация потока"""
        Thread.__init__(self)
        self.value = value
    def run(self):
        """Запуск потока"""
        return ping(self.value)

class TerminalTimeout(Thread):
    def __init__(self, value):
        """Инициализация потока"""
        Thread.__init__(self)
        self.value = value
    def run(self):
        """Запуск потока"""
        print('start')
        # Сессия открыта 10 минут, если баланс 0 то закрываем
        while True:
            time.sleep(600)
            session = Session.objects.get(sessionId=self.value)
            print(session.balance)
            if int(session.balance) == int(0):
                session.status = Status.objects.get(pk=4)
                session.save()
                break
        print('stop')
        

class TerminalView(View):

    def get(self, request, suburl='', pk=''):
        if suburl == 'add':
            form = TerminalForm()
            return render(request, 'terminal.html', {'form': form})

        if suburl == 'edit':
            term = Terminal.objects.get(pk=pk)
            form = TerminalForm(instance=term)
            return render(request,'terminal.html', {'form': form})

        if suburl == 'del':
            Terminal.objects.get(pk=pk).delete()
            return redirect('/terminals/')

        actives = Terminal.objects.all().values_list('ipAddress', flat=True)
        for active in actives:
            ping = ThreadCustom(active)
            ping.start()
        terminals = Terminal.objects.all()
        data = {
            'terminals': terminals
        }
        return render(request, 'terminals.html', data)
    
    def post(self, request, suburl='', pk=''):
        if suburl == 'add':
            form = TerminalForm(request.POST)
            if form.is_valid:
                form.save()
                return redirect('/terminals/')
        if suburl == 'edit':
            term = Terminal.objects.get(pk=pk)
            form = TerminalForm(self.request.POST, instance=term)
            if form.is_valid:
                form.save()
                return redirect('/terminals/')
        return redirect('/terminals/')


class SessionView(View):
    template = 'sessions.html'

    def get(self, request, suburl='', pk=''):
        # client_ip = checkIpAddress(request.META['REMOTE_ADDR'])
        client_ip = request.META['REMOTE_ADDR']
        # client_ip = request.META.get('HTTP_X_FORWARDED_FOR', '')
        print(client_ip)
        request.session["fav_color"] = "blue"
        print(request.COOKIES.get('logged_in_status'))
        if suburl == 'add':
            form = SessionForm()
            return render(request, 'session.html', {'form': form})

        if suburl == 'edit':
            term = Session.objects.get(pk=pk)
            form = SessionForm(instance=term)
            return render(request,'session.html', {'form': form})

        if suburl == 'del':
            Session.objects.get(pk=pk).delete()
            return redirect('/sessions_all/')

        if 'status' in request.GET.keys():
            sessions = Session.objects.filter(status=request.GET['status'])
        else:
            sessions = Session.objects.all()
        
        response = render_to_response(self.template, {'sessions': sessions, 'user': request.user})
        response.set_cookie('logged_in_status', 'never_use_this_ever') 
        return response
        # return render(request, self.template, {'sessions': sessions})

    def post(self, request, suburl='', pk=''):
        if suburl == 'add':
            form = SessionForm(request.POST)
            if form.is_valid:
                form.save()
                return redirect(request.POST['path'])
        if suburl == 'edit':
            term = Session.objects.get(pk=pk)
            form = SessionForm(self.request.POST, instance=term)
            if form.is_valid:
                form.save()
                return redirect(request.POST['path'])
        return redirect(request.POST['path'])

class SessionViewAll(SessionView):
    template = 'sessions_all.html-new'
