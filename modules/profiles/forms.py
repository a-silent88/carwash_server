from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.contrib.auth.hashers import (
    UNUSABLE_PASSWORD_PREFIX, identify_hasher,
)
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.text import capfirst
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.contrib.auth.forms import SetPasswordForm
from django.forms import ModelForm
# from phone_field import PhoneField, PhoneWidget, PhoneFormField
UserModel = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserCreationForm, self).__init__(*args, **kargs)
        # del self.fields['username']

    class Meta:
        model = CustomUser
        fields = ("email",)
    
class CustomUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)
        # del self.fields['username']

    class Meta:
        model = CustomUser
        fields = ("email",)

class CustomSetPasswordForm(SetPasswordForm):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    new_password1 = forms.CharField(
        label=_(""),
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Новый пароль'
                }
        ),
        strip=False,
        help_text='',
    )
    new_password2 = forms.CharField(
        label=_(""),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Повторите пароль еще раз'
                }
        ),
    )
# class CustomPhoneFormField(PhoneFormField):
#     widget = PhoneWidget

class CustomUserForm(forms.ModelForm):

    first_name = forms.CharField(
        label=_(""),
        max_length=200, 
        # help_text='Required - email',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Имя'
            }
        ),
        )
    last_name = forms.CharField(
        label=_(""),
        max_length=200, 
        # help_text='Required - email',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Фамилия'
            }
        ),
        )
    phone = forms.CharField(
        label=_(""),
        max_length=12, 
        # help_text='Required - email',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Телефон'
            }
        ),
        )
    def __init__(self, *args, **kargs):
        super(CustomUserForm, self).__init__(*args, **kargs)
        
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'phone')

class ChangeUsersProfiles(CustomUserForm):
    is_active = forms.BooleanField(
        label=_("Доступ в Веб-интерфейс"),
        # help_text='Required - email',
        widget=forms.CheckboxInput(),
        required=False
        )
    def __init__(self, *args, **kargs):
        super(ChangeUsersProfiles, self).__init__(*args, **kargs)
        self.fields['phone'].label = 'Телефон'
        self.fields['phone'].widget.attrs['placeholder'] = 'Телефон'
        self.fields['phone'].widget.attrs['required'] = 'True'
        self.fields['phone'].help_text = None

        self.fields['email'].label = 'E-mail'
        self.fields['email'].widget.attrs['placeholder'] = 'E-mail'
        self.fields['email'].help_text = None

        self.fields['first_name'].label = 'Имя'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Имя'
        self.fields['first_name'].help_text = None

        self.fields['last_name'].label = 'Фамилия'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Фамилия'
        self.fields['last_name'].help_text = None

        self.fields['balance'].label = 'Баланс'
        self.fields['balance'].widget.attrs['placeholder'] = 'Баланс'
        self.fields['balance'].help_text = None

        self.fields['cardId'].label = 'ID карты'
        self.fields['cardId'].widget.attrs['placeholder'] = 'ID карты'
        self.fields['cardId'].help_text = None

        self.fields['groups'].label = 'Группа'
        self.fields['groups'].help_text = None

    class Meta:
        model = CustomUser
        fields = ('phone', 'first_name', 'last_name', 'email', 'groups', 'balance', 'cardId', 'is_active', 'cardNumber')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.instance.first_name = self.cleaned_data.get('first_name')
        self.instance.last_name = self.cleaned_data.get('last_name')
        self.instance.email = self.cleaned_data.get('email')
        self.instance.phone = self.cleaned_data.get('phone')
        self.instance.is_active = self.cleaned_data.get('is_active')
        self.instance.cardNumber = self.cleaned_data.get('cardNumber')
        self.instance.save()


class CustomAddUser(ChangeUsersProfiles):
    def __init__(self, *args, **kargs):
        super(CustomAddUser, self).__init__(*args, **kargs)

    class Meta:
        model = CustomUser
        fields = ('phone', 'first_name', 'last_name', 'email', 'groups', 'balance', 'cardId', 'is_active', 'cardNumber')

