
from django import forms
from django.contrib.auth.models import User
from django.template import loader
from django.utils.translation import gettext, gettext_lazy as _
from .models import Pay
from django.forms import ModelForm
from django.core.exceptions import ValidationError

class PayFormAdd(ModelForm):
 
    class Meta:
        model = Pay
        fields = ['client', 'price']

    def __init__(self, *args, **kargs):
        super(PayFormAdd, self).__init__(*args, **kargs)
        self.fields['price'].widget.attrs['placeholder'] = 'Введите сумму'
        self.fields['client'].widget.attrs['type'] = 'hidden'