from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin, UserManager
from django.utils.translation import ugettext_lazy as _
from .customUserManager import CustomUserManager
from django.utils import timezone
from django_countries.fields import CountryField
from django.core.mail import send_mail

class MyUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(_('email address'), max_length = 40, unique= True)
    username = models.CharField(_('username'),max_length = 30,unique = True)
    first_name = models.CharField(_('first name'),max_length= 30,blank = True)
    last_name = models.CharField(_('last name'),max_length=30,blank = True)
    date_joined = models.DateTimeField(_('date joined'),default= timezone.now)
    last_login = models.DateTimeField(_('last login'),auto_now_add=True)
    is_superuser = models.BooleanField(_('is superuser'),default = False)
    is_staff = models.BooleanField(_('is staff'),default = False)
    is_active = models.BooleanField(_('is active'),default = True)
    objects = CustomUserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.username
    
    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
    

    
