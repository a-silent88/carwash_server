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
        #print(request.data)
        #Сделать try
        session = Session.objects.get(sessionId=request.data['sessionId'])
        terminal = Terminal.objects.get(terminalId=request.data['terminalId'])
        service = Service.objects.get(code=request.data['service'])
        status_session = request.data['status']
        try:
            service_pk = session.service.pk
        except:
            service_pk = None

        if 'action' in request.data:
            if request.data['action'] == 'bindsession':
                id_client = request.data['clientId']
                try:
                    client = get(cardId=id_client)
                except:
                    client = get(pk=id_client)
                else:
                    pass
                session.clientId = client.pk
                answer = {'balance': int(client.balance)}
                return answer
            if request.data['action'] == 'stopsession':
                session.status = 2
                answer = {'action': 'stopsession',
                          'balance': 0,
                          'clientId': '0',
                          }
                return Response(answer)
            
            if request.data['action'] == 'prices':
                services = service.objects.all()
                # services.id for services in service.objects.all()
                return Response(json.dumps(services), status=status.HTTP_201_CREATED)
        else:
            data = {
                'action': 'Input type-request',
            }
            return Response(data)