from django.http import HttpResponse
from django.shortcuts import render, redirect
# Create your views here.
from rest_framework import routers, serializers, viewsets
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import filters as filter_search
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
import json
from django_filters import rest_framework as filters
from modules.terminal.models import Terminal, Session, Status, StatusTerminal
from modules.service.models import Service
from modules.profiles.models import CustomUser
from modules.terminal.views import TerminalTimeout
from main.models import Setting

# user = CustomUser.objects.get(pk=1)
# token = Token.objects.get(user=user)
def genId():
    import random 
    import string 
    return ''.join([random.choice(string.digits) for n in range(16)]) 

class TerminalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terminal
        fields = ('pk','terminalId', 'name', 'balance', 'status', 'ipAddress')

class TerminalList(viewsets.ModelViewSet):
    queryset = Terminal.objects.all()
    serializer_class = TerminalSerializer
    filter_backends = (filter_search.SearchFilter,)
    search_fields = ('terminalId', 'status')

class SessionSerializer(serializers.ModelSerializer):
    terminalId = serializers.CharField()
    clientId = serializers.CharField()
    class Meta:
        model = Session
        fields = ('pk','sessionId', 'terminalId', 'status', 'clientId', 'service', 'balance')

class SessionSerializerCustom(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ('pk','sessionId', 'terminalId', 'status', 'clientId', 'service', 'balance')

class SessionList(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    filter_backends = (filter_search.SearchFilter,)
    search_fields = ('sessionId', 'status')

class SessionApi(APIView):
    def get(self, request, format=None):
        if 'terminalId' in request.GET.keys():
            terminal_id = request.GET['terminalId']
            try:
                terminal_pk = Terminal.objects.filter(terminalId=terminal_id).values_list('pk', flat=True)[0]
                sessions = Session.objects.filter(Q(terminalId=terminal_pk) & Q(status=1))
                if list(sessions) == []:
                    terminal = Terminal.objects.get(terminalId=terminal_id)
                    print(terminal.status)
                    if str(terminal.status) != "Активен":
                        data = {
                            'terminalId' : 'Терминал не активен',
                        }
                        return Response(data)
                    session_id = genId()
                    sessions_new = Session.objects.create(
                        sessionId=session_id,
                        terminalId=terminal,
                        status=Status.objects.get(pk=1)
                    )
                    sessions_new.save()
                    sessions = Session.objects.filter(sessionId=session_id)
                    timeout = TerminalTimeout(session_id)
                    timeout.start()
            except IndexError:
                data = {
                    'terminalId' : 'Терминал не подключен',
                }
                return Response(data)
        else:
            data = {
                'terminalId' : 'Введие ID терминала',
            }
            return Response(data)
        serializer = SessionSerializer(sessions, many=True)
        return Response(serializer.data)
        
    def post(self, request, format=None):
        print(request.data)
        #Сделать try
        session = Session.objects.get(sessionId=request.data['sessionId'])
        terminal = Terminal.objects.get(terminalId=request.data['terminalId'])
        service = Service.objects.get(code=request.data['service'])
        status_session = request.data['status']
        try:
            service_pk = session.service.pk
        except:
            service_pk = None
            ##########
        def changeClient(id_client, **kwargs):
            print(id_client)
            try:
                client = get(cardId=id_client)
            except:
                client = get(pk=id_client)
            else:
                pass
            
            if 'action' in kwargs:
                if kwargs['action'] == 'clientAdd': 
                    return client.pk
                if kwargs['action'] == 'clientBalance': 
                    return int(client.balance)
                if kwargs['action'] == 'clientChangeBalance':
                    if 'balance' in kwargs and 'status' in kwargs:
                        if kwargs['status'] != 2:
                            client.balance = int(kwargs['balance'])
                            client.save()
                        else:
                            client.balance = int(kwargs['balance'])
                            client.save()
                        return int(client.balance)
##########        
        request.data['terminalId'] = terminal.pk
        request.data['service'] =  service.pk
        if 'clientId' in request.data:
            request.data['clientId'] = changeClient(request.data['clientId'], action='clientAdd')
            balance = changeClient(request.data['clientId'], action='clientBalance')
            request.data.update({'balance': balance})
            request.data.update({'balance_add_user': True})

        if 'balance' in request.data:
            if 'balance_add_user' in request.data:
                terminal.balance = int(session.balance) + request.data['balance']
            elif request.data['status'] != 2:
                terminal.balance = int(terminal.balance) + request.data['balance']
            else:
                if session.clientId == None or session.clientId == 'null':
                    main_balance = Setting.objects.get(pk=1)
                    main_balance.balance = int(main_balance.balance) + int(request.data['balance'])
                    main_balance.save()
                    terminal.balance = 0
                else:
                    terminal.balance = 0
            terminal.save()
            if 'clientId' in request.data:
                request.data['balance'] = changeClient(request.data['clientId'], action='clientChangeBalance', balance=terminal.balance, status=status_session)
            else:
                if session.clientId != None and service_pk == service.pk:
                    if request.data['status'] != 2:
                        request.data['balance'] = changeClient(session.clientId.pk, action='clientChangeBalance', balance=terminal.balance, status=status_session)
                    else:
                        request.data['balance'] = changeClient(session.clientId.pk, action='clientChangeBalance', balance=request.data['balance'], status=status_session)
                else:
                    if service_pk != service.pk and (request.data['balance']) <= int(session.balance):
                        terminal.balance = request.data['balance']
                        terminal.save()
                        if session.clientId != None:
                            request.data['balance'] = changeClient(session.clientId.pk, action='clientChangeBalance', balance=request.data['balance'], status=status_session)
                    else:
                        request.data['balance'] = terminal.balance
        serializer = SessionSerializerCustom(session, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'sessionId': request.data['sessionId'],
                'balance': request.data['balance'],
                'service': service.code,
                'action': 'update'
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)