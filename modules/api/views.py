from django.http import HttpResponse, JsonResponse
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
from modules.terminal.models import Terminal, Session, Status, StatusTerminal, Usage
from modules.service.models import Service
from modules.profiles.models import CustomUser, CustomUserManager, ClientCards
from modules.terminal.views import TerminalTimeout
from modules.paysystem.models import Pay
from datetime import datetime
from dateutil import tz
from modules.profiles.forms import CustomAddUser
from datetime import timedelta
import pytz
from django.utils import timezone
from main.models import Setting
from django.db.models import Sum, Avg
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


# class AddUser(APIView):
#     def post(self, request, format=None):
#         print(request.data)
#         clientsCards = ClientCards.objects.get(cardNumber=request.data["cardNumber"])
#         request.data['cardId'] = clientsCards.cardId
#         form_add_user = CustomAddUser(request.data)
#         if form_add_user.is_valid():
#             form_add_user.save()
#             clientsCards.is_active = True
#             clientsCards.save()
#             return HttpResponse(content="True", status=200)
#         else:
#             print("add_user_form no valid")
#             return HttpResponse(content="False", status=404)

class AddUser(APIView):
    def post(self, request, format=None):
        # print(request.data)
        asdf = CustomUser.objects.filter(phone__regex=r'^[\+7|8]*?\d{10}$').values('phone')
        print(list(asdf))
        # s = CustomUser.get_phone(phone__regex=r'\+')
        # print(s)
        # ans =
        # form_add_user = CustomAddUser(request.data)
        return Response(200)


class DelUser(APIView):
    def get(self, request):
        if request.GET["cardNumber"] != "" and request.GET["cardNumber"] is not None:
            try:
                delete_user = CustomUser.objects.get(cardNumber=request.GET["cardNumber"])
            except:
                print("Пользователя с такой картой не существует")
                return HttpResponse(content="Not exist", status=404)
            print(delete_user)
            delete_user.groups.clear()
            delete_user.delete()
            print("user with cardNumber: ", request.GET["cardNumber"], "deleted")
            return HttpResponse(content="True", status=200)
        else:
            print("api.DelUser: request.GET[\"cardNumber\"] == \"\" or None")
            return HttpResponse(content="False", status=404)


class AddCard(APIView):
    def get(self, request):
        cardNumber = request.GET['cardNumber']
        cardId = request.GET['card_id']
        print(type(cardNumber))
        print(type(cardId))
        try:
            ClientCards.objects.create(cardNumber=cardNumber, cardId=cardId, is_active=True)
            return Response("Ok")
        except:
            return Response("False")


class SessionApi(APIView):
    def get(self, request, format=None):
        if 'cardId' in request.GET.keys():
            try:
                clientId = CustomUser.objects.get(cardId=request.GET['cardId'])
            except:
                return Response({"result": 0})
            else:
                return Response({"result": 1})

        if 'prices' in request.GET.keys():
            services = list(Service.objects.values('code','price'))
            answer = {}
            for i in range(len(services)):
                answer[services[i]['code']] = services[i]['price']
            return Response(answer)
        if 'terminalId' in request.GET.keys():
            terminal_id = request.GET['terminalId']
            try:
                terminal_pk = Terminal.objects.filter(terminalId=terminal_id).values_list('pk', flat=True)[0]
                sessions = Session.objects.filter(Q(terminalId=terminal_pk) & Q(status=1))
                #если приходит новый запрос на открытие сессии. закрываем старую сессию и открываем новую
                if list(sessions) != []:
                    print(sessions)
                    Session.objects.filter(Q(terminalId=terminal_pk) & Q(status=1)).update(status=2)
                terminal = Terminal.objects.get(terminalId=terminal_id)
                print(terminal.status)
                '''
                if str(terminal.status) != "Активен":
                    data = {
                        'terminalId' : 'Терминал не активен',
                    }
                    return Response(data)
                '''
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
        def selectClient(id_client):
            print(id_client)
            try:
                client = CustomUser.objects.get(cardId=id_client)
            except:
                client = CustomUser.objects.get(pk=id_client)
            else:
                pass
            return(client)

        #print(request.data)
        #Сделать try
        session = Session.objects.get(sessionId=request.data['sessionId'])
        terminal = Terminal.objects.get(terminalId=request.data['terminalId'])
        try:
            service_pk = session.service.pk
        except:
            service_pk = None

        if 'action' in request.data:
            if request.data['action'] == 'bindsession':
                try:
                    client = selectClient(request.data['clientId'])
                    session.clientId = client
                except:
                    answer = {'balance': -1}
                    return Response(answer)
                print(session.clientId)
                session.balance += int(client.balance)
                session.save()
                answer = {'balance': int(client.balance)}
                return Response(answer)
            if request.data['action'] == 'stopsession':
                status_session = '2'#request.data['status']
                session.status = Status.objects.get(id=status_session)
                #print(session)
                price_session = Usage.objects.filter(sessionId_id=session).aggregate(Sum('price'))
                session.balance = price_session['price__sum']  #'price__sum'
                session.save()

                if session.clientId is None or session.clientId == 'null' or session.clientId == '0' or session.clientId == 0:
                    print('ClientId = NULL')
                    answer = {'action': 'stopsession',
                              'balance': 0,
                              'clientId': '0'
                              }
                    return Response(answer)
                else:
                    print('ClientId != NULL')
                    client = selectClient(session.clientId.pk)
                    print(client)
                    client.balance = request.data['balance']
                    client.save()
                    return Response('Session stop')
            if request.data['action'] == 'prices':
                services = list(Service.objects.values('code','price'))
                answer = {}
                for i in range(len(services)):
                    answer[services[i]['code']] = services[i]['price']
                return Response(answer)
            if request.data['action'] == 'payment':
                session.balance += request.data['balance']
                session.save()
                terminal.balance += request.data['balance']
                data = {'balance': session.balance}

                pay = Pay(price=request.data['balance'])
                timezone.activate(pytz.timezone('Asia/Yekaterinburg'))
                if session.clientId is not None or session.clientId != 'null' or session.clientId != '0' or session.clientId != 0:
                    pay.client = session.clientId
                # TZ = tz.gettz("UTC+5")
                # TZ = tz.gettz("Asia / Yekaterinburg")
                now_date = datetime.now()
                print(now_date)
                pay.date = now_date
                pay.save()

                return Response(data)

            if request.data['action'] == 'serviceUsage':
                print("Pushbatton:")
                print("service", request.data['service'])
                print("duration", request.data['duration'])
                print("price", request.data['price'])

                service = Service.objects.get(code=request.data['service'])
                serviceUsage_new = Usage.objects.create(sessionId=session, service=service, duration=request.data['duration'],price=request.data['price'])
                serviceUsage_new.save()
                return Response('ok')



            else:
                data = {'action': 'unknown', }
                return Response(data)
        else:
            data = {
                'action': 'null',
            }
            return Response(data)

from django.db.models.functions import TruncMonth
from django.db.models import Count

class GetPays(APIView):
    def get(self, request):
        my_tz = pytz.timezone("Asia/Yekaterinburg")
        if "today" in request.GET.keys():
            today = datetime.now(tz=my_tz)
            try:
                q = Pay.objects.filter(date__day=today.day).values('price')
            except:
                return Response("GetPays: no data")
            answer = list(q)
            _sum = 0
            for key in answer:
                _sum += int(key['price'])
            print(_sum)
            return Response(_sum)

        if "yesterday" in request.GET.keys():
            yesterday = datetime.now(tz=my_tz) - timedelta(days=1)
            try:
                q = Pay.objects.filter(date__day=yesterday.day).values('price')
            except:
                return Response("GetPays: no data")
            answer = list(q)
            _sum = 0
            for key in answer:
                _sum += int(key['price'])
            print(_sum)
            return Response(_sum)

        if "month" in request.GET.keys():
            month = request.GET['month']
            try:
                query = Pay.objects.values('price').filter(date__month=month)
            except:
                return Response("GetPays: no records")
            ans = list(query)
            print(type(ans))
            print(ans)
            ans = list(query)
            _sum = 0
            for key in ans:
                _sum += int(key['price'])
            return Response(_sum)
