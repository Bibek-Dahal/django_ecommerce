from django.contrib import admin
from django.urls import path,include
from .import views
app_name = 'store'
urlpatterns = [
    path('',views.Home,name = "home"),
    path('product/<slug:slug>/',views.ProductDetailView.as_view(),name = 'product_detail'),
    path('catagory/<slug:slug>/',views.CatagoryView.as_view(),name = 'catagory_detail'),
    path('products/<slug:slug>/',views.ProductListView.as_view(),name='products'),
    
    

]

