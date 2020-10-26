from django.db import models
from django.utils import timezone
from modules.profiles.models import CustomUser
from django.utils.translation import ugettext_lazy as _
# Create your models here.

class Service(models.Model):
    code = models.CharField(_("Код услуги"), max_length=20, blank=True, null=True)
    name = models.CharField(_("Название услуги"), max_length=500, blank=True, null=True)
    unit = models.CharField(_("Ед. Измерения"), max_length=10, blank=True, null=True)
    price = models.CharField(_("Стоимость"), max_length=50, blank=True, null=True)
    def __str__(self):
        return self.name
    objects = models