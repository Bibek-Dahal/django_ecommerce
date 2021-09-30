
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from allauth.socialaccount.providers.google import views

urlpatterns = [
    path('bibek/ecom/admin/', admin.site.urls),
    path('',include('store.urls',namespace= 'store')),
    path('cart/',include('cart.urls',namespace='cart')),
    # path('accounts/',include('allauth.urls')),
    path('account/',include('user_account.urls',namespace='account')),
    
]
# + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)