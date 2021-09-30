from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','user','order_id','customer','product','quantity','price','variation','created_at','status']
