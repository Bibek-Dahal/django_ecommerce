from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Customer, Product,Product_image
from django.contrib.auth.models import User



@receiver(post_save,sender=User)
def add_customer(sender,instance,created,**kwargs):
    if created:
        Customer.objects.create(user=instance)

# @receiver(post_save,sender=Customer)
# def add_cart(sender,instance,created,**kwargs):
#     if created:
#         Cart.objects.create(customer=instance)

