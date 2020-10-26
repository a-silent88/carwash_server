from django.db import models
from django.utils import timezone
from modules.profiles.models import CustomUser
from django.utils.translation import ugettext_lazy as _
from modules.service.models import Service
# Create your models here.


class Status(models.Model):
    name = models.CharField(_("Статус сессии"), max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name
    objects = models


class StatusTerminal(models.Model):
    name = models.CharField(_("Статус терминала"), max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name
    objects = models


class Terminal(models.Model):
    terminalId = models.CharField(_("ID"), max_length=20, blank=True, null=True)
    name = models.CharField(_("Название"), max_length=100, blank=True, null=True)
    balance = models.IntegerField(_("Баланс"), default=0, blank=True, null=True) # баланс терминала показывает сколько денег находится в кассете
    status = models.ForeignKey(StatusTerminal, on_delete=models.SET_DEFAULT, default='', blank=True, null=True)
    ipAddress = models.CharField(_("IP адрес"), max_length=20, blank=True, null=True)

    def __str__(self):
        return self.terminalId
    objects = models


class Session(models.Model):
    sessionId = models.CharField(_("ID"), max_length=20, blank=True, null=True)
    terminalId = models.ForeignKey(Terminal, on_delete=models.SET_DEFAULT, default='', blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.SET_DEFAULT, default='', blank=True, null=True)
    clientId = models.ForeignKey(CustomUser, on_delete=models.SET_DEFAULT, default='', blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.SET_DEFAULT, default='', blank=True, null=True)
    balance = models.IntegerField(_("Баланс"), default=0, blank=True, null=True)

    def __str__(self):
        return self.sessionId
    objects = models

    def __init__(self, *args, **kwargs):
        super(Session, self).__init__(*args, **kwargs)
        self.count = Status.objects.all().count()
        if self.count == 0:
            model = Status
            model.objects.create(
                name='Открыта'
            )
            model.objects.create(
                name='Закрыта'
            )


class Usage(models.Model):
    sessionId = models.ForeignKey(Session, on_delete=models.SET_NULL, default='', blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.SET_DEFAULT, default='', blank=True, null=True)
    duration = models.IntegerField(_("Длительность"), default=0, blank=True, null=True)
    price = models.IntegerField(_("Стоимость услуги"), default=0, blank=True, null=True)

    def __str__(self):
        return self.sessionId
    objects = models.Manager()
