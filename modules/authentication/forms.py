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
from ..profiles.models import CustomUser
from django.contrib.auth.forms import SetPasswordForm
# from phone_field import PhoneField, PhoneWidget, PhoneFormField
UserModel = get_user_model()

class MyAuthenticationForm(AuthenticationForm):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    username = UsernameField(
        label=_(""),
        widget=forms.TextInput(
            attrs={
                'autofocus': True,
                'placeholder': 'Номер телефона'
                }))
    password = forms.CharField(
        label=_(""),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Пароль'
            }
        ),
    )
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        # Set the max length and label for the "username" field.
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        self.fields['username'].max_length = self.username_field.max_length or 254
        if self.fields['username'].label is None:
            self.fields['username'].label = capfirst(self.username_field.verbose_name)

class SignupForm(UserChangeForm):
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
    password = None

    def __init__(self, *args, **kargs):
        super(SignupForm, self).__init__(*args, **kargs)

    class Meta:
        model = CustomUser
        fields = ('phone',)
