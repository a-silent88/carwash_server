from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
# from index.models import Order
# from .forms import ChangeUsersProfiles
# from phone_field import PhoneField


class CustomUserManager(BaseUserManager):
    def _create_user(self, phone, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not phone:
            raise ValueError('The given phone must be set')

        user = self.model(phone=phone,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        return self._create_user(phone, password, False, False,
                                 **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        return self._create_user(phone, password, True, True,
                                 **extra_fields)

# Класс описивающий карты выданные в обращение находящиеся у администратора или выданные клиентам
class ClientCards(models.Model):
    cardNumber = models.IntegerField(_("Номер на карте"), default=0, blank=True, null=True)
    cardId = models.CharField(_("ИД карты клиента"), max_length=20, default=0,  blank=True, null=True)
    is_active = models.BooleanField(_("Выдана клиенту"), default= False, help_text="Выдана ли карта клиенту")

    def __str__(self):
        return self.cardNumber
    objects = models.Manager()


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    A fully featured User model with admin-compliant permissions that uses
    a full-length email field as the username.

    Email and password are required. Other fields are optional.
    """
    email = models.EmailField(_('email address'), max_length=254, blank=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    phone = models.CharField(_('phone'), max_length=12, unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False, help_text=_('Designates whether the user can log into this admin '
                                                                                 'site.'))
    is_active = models.BooleanField(_('active'), default=False, help_text=_('Designates whether this user should be treated as '
                                                                            'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    balance = models.CharField(_("Баланс клиента"), max_length=20, default=0,  blank=True, null=True)
    cardId = models.CharField(_("ИД карты клиента"), max_length=20, default=0,  blank=True, null=True)
    objects = CustomUserManager()
    telegram_id = models.IntegerField(blank=True, null=True)
    cardNumber = models.IntegerField(blank=True, null=True)
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.phone)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def get_phone(self):
        "Returns the short name for the user."
        return self.phone

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    def __str__(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()


