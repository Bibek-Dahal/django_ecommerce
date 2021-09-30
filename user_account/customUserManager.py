from django.contrib.auth.models import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.db import models
class CustomUserManager(BaseUserManager):

    def create_user(self,email,username,password,**extra_fields):
        if not email:
            raise ValueError(_('Email must be set'))
            
        email = self.normalize_email(email)
        user = self.model(email = email,username = username,**extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,email,username,password,**extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('The staff status must be true'))

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('The superuser status must be true'))
        if extra_fields.get('is_active') is not True:
            raise ValueError(_('The active status must be true'))

        return self.create_user( email,username,password,**extra_fields)

        

