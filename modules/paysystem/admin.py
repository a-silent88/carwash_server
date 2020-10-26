from django.contrib import admin

# # Register your models here.
from .models import Pay, StatusPay
admin.site.register(Pay)
admin.site.register(StatusPay)