from django import forms
import re
from django.contrib.auth.backends import UserModel
# from django.core.validators import validators
from django.core.exceptions import ValidationError
from django.forms import widgets
from django.forms.fields import EmailField
from django.utils.translation import ugettext_lazy as _
from .models import MyUser
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm,SetPasswordForm
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django_countries import countries
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from store.models import Customer
from django.core.exceptions import ValidationError
from django.utils.text import capfirst

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(min_length=3,widget=forms.TextInput(attrs={"class": "form-control","placeholder":"enter your name"}))
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        max_length=25,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control','placeholder':'enter password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )  
    password2 = forms.CharField(
            label=_("Password confirmation"),
            widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control','placeholder':'re-enter password'}),
            max_length=25,
            strip=False,
            help_text=_("Enter the same password as before, for verification."),
    )   
    class Meta:
        model = MyUser
        fields = ('email','username')
    
        widgets ={
            # 'country':CountrySelectWidget(attrs={"class": "form-select"}),
            'email':forms.EmailInput(attrs={"class": "form-control","placeholder":"enter your email","minlength":11}),
            # 'username':forms.TextInput(attrs={"class": "form-control","placeholder":"enter your name","minlength":3})
            #'password':forms.PasswordInput(attrs={"class": "form-control"})
        }
       

    def clean_username(self):
        
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        check_username = re.findall("[a-zA-Z]",cleaned_data.get('username'))
        if not check_username:
            raise ValidationError('Enter valid username')
        print(username)
        return username

    def clean_password2(self):
        super().clean()
        pwd = self.cleaned_data.get('password1')
        print()
        print('pwd',pwd)
        print('Lem',len(pwd))
        if len(pwd) >= 8:
            reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
            pat = re.compile(reg)
            mat = re.search(pat, pwd)
            if not mat:
                raise ValidationError('Password must contain atleats one digit special characrers and uppercase letter')
            return pwd
        
                    
        
class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = MyUser
        fields = ('email',)

class CustomUserLoginForm(forms.Form):
    
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    email = EmailField(widget=forms.EmailInput(attrs={'autofocus': True,'class':'form-control'}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password','class':'form-control'}),
    )

    error_messages = {
        'invalid_login': _(
            "Please enter a correct email and password."
            
        ),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        # Set the max length and label for the "username" field.
        self.email_field = UserModel._meta.get_field(UserModel.EMAIL_FIELD)
        email_max_length = self.email_field.max_length or 254
        self.fields['email'].max_length = email_max_length
        self.fields['email'].widget.attrs['maxlength'] = email_max_length
        if self.fields['email'].label is None:
            self.fields['email'].label = capfirst(self.email_field.verbose_name)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'username': self.email_field.verbose_name},
        )

        
class PWDResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email','class':'form-control'})
    )
    class Meta:
        model = MyUser

class SetPWDForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}),
    )
    class Meta:
        model = MyUser

    def clean_new_password2(self) -> str:
        new_pwd = super().clean_new_password2()
        print('inside new models  ffafjf ')
        # new_pwd = self.cleaned_data.get('password2')
        print('new_pwd',new_pwd)
        print()
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
        pat = re.compile(reg)
        mat = re.search(pat, new_pwd)
        if not mat:
            raise ValidationError('Password must contain atleats one digit special characrers and uppercase letter')
        return new_pwd

class PwdChangeForm(PasswordChangeForm,SetPWDForm):
    error_messages = {
        **SetPWDForm.error_messages,
        'password_incorrect': _("Your old password was entered incorrectly. Please enter it again."),
    }
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True,'class':'form-control'}),
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}),
    )
    

class CustomerRegForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('full_name','phone_number','temporary_address','shipping_address')
        widgets={
            'full_name':forms.TextInput(attrs={"class": "form-control","placeholder":"enter your full name"}),
            'phone_number':forms.TextInput(attrs={'class':'form-control',"placeholder":"enter phone number"}),
            'temporary_address':forms.TextInput(attrs={"class": "form-control","placeholder":"enter your temporary_address"}),
            'shipping_address':forms.TextInput(attrs={"class": "form-control","placeholder":"enter your shipping_address"})
        }
    def clean_phone_number(self):
        cleaned_data = super().clean()
        ph_num = cleaned_data.get('phone_number')
        print(ph_num)
        print(ph_num.isnumeric())
        if not len(ph_num)<10:
            if not ph_num.isnumeric():
                raise ValidationError('Enter valid phone number')
            
            return ph_num
        else:
            raise ValidationError('Enter valid phone number')
        # return ph_num
            

