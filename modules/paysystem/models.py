from django.db import models
from django.utils import timezone
from modules.profiles.models import CustomUser
from django.utils.translation import ugettext_lazy as _
# Create your models here.




class StatusPay(models.Model):
    name = models.CharField(_("Статус"), max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name
    objects = models


class Pay(models.Model):
    status = models.ForeignKey(StatusPay, on_delete=models.SET_DEFAULT, default='', blank=True, null=True)
    client = models.ForeignKey(CustomUser, on_delete=models.SET_DEFAULT, default='', blank=True, null=True)
    price = models.CharField(_("Сумма платежа"), max_length=20, blank=True, null=True)
    date = models.DateTimeField(_("Время платежа"), blank=True)

    def __str__(self):
        return self.client
    objects = models.Manager()


class Incas(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_DEFAULT, default='', blank=True, null=True)
    date = models.DateTimeField(_("Дата инкассации"))
    type = models.CharField(_("Тип инкассации"), max_length=20, default='', blank=True)

    def __str__(self):
        return self.user
    objects = models.Manager()

