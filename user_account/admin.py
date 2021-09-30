from django.contrib import admin
from .models import MyUser
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
# Register your models here.
from .forms import CustomUserCreationForm
# @admin.register(MyUser,UserAdmin)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ['id','username','email','is_active']


# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = MyUser
    add_form = CustomUserCreationForm
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ( 'date_joined',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email', 'password1', 'password2'),
        }),
    )


admin.site.register(MyUser, CustomUserAdmin)