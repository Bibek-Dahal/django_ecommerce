from django.urls import path
from .import views
app_name = 'account'
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('signin/',views.SignInView.as_view(),name='signin'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('password_reset/', views.PwdResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PwdResetConfirmView.as_view(), name='password_reset_confirm'),
    path('account_activate/<slug:uidb64>/<slug:token>/',views.account_activate,name='activate'),
    path('password_change/',views.PwdChangeFormView.as_view(),name='password_change'),
    path('reset/done/', views.PwdResetCompleteView.as_view(), name='password_reset_complete'),
    path('customer/registration/',views.CustomerRegView.as_view(),name='customer_reg'),
    path('profile/edit/<slug:uuid>/',views.ProfileEditView.as_view(),name='profile_edit'),
    path('customer/profile/',views.ProfileView.as_view(),name='profile'),
    
    
]