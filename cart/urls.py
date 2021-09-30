from django.urls import path,include
from .import views
app_name = 'cart'
urlpatterns = [
    path('add-to-cart/',views.AddToCartView.as_view(),name='addToCart'),
    path('cart-detail/',views.CartDetailView.as_view(),name='cartDetail'),
    path('verify/',views.VerifyKhalthiView.as_view(),name="verify_khalthi"),
    path('remove-cart/',views.RemoveCartView.as_view(),name="reomveCart"),
    path('buy-products/',views.BuyProducts.as_view(),name='buy'),
    path('order/',views.OrderView.as_view(),name='order'),
    path('v-esewa/',views.VerifyEsewa.as_view(),name='virify-esewa'),
    path('my-order/',views.MyOrderView.as_view(),name="my_order"),
    path('transaction-failed/',views.FailuereOrderView.as_view(),name="fail_trans"),
    path('disp_img/',views.DispImg.as_view(),name='disp_img'),
    
]