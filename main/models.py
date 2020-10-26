from django.db import models
from django.utils import timezone
from modules.profiles.models import CustomUser
from django.utils.translation import ugettext_lazy as _
from modules.service.models import Service
# Create your models here.

class Setting(models.Model):
    name = models.CharField(_("Название системы"), max_length=20, blank=True, null=True)
    balance = models.CharField(_("Баланс системы"), default=0, max_length=20, blank=True, null=True)
    def __str__(self):
        return self.name
    objects = models
