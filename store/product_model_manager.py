# from django.contrib.auth.models import BaseUserManager
from django.db import models

class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_stock = True)
