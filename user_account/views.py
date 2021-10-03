import autoslug
from django.contrib.auth import views
import requests
from django.shortcuts import redirect, render,HttpResponse,HttpResponseRedirect
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.template.loader import render_to_string
from .forms import CustomUserLoginForm,CustomUserCreationForm,CustomerRegForm,PwdChangeForm
from .models import*
from django.contrib.auth.views import LoginView, PasswordChangeView,PasswordResetView,PasswordResetDoneView,PasswordResetCompleteView,PasswordResetConfirmView
from django.contrib.auth import authenticate, login
from .forms import PWDResetForm,SetPWDForm
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import TemplateView, View
import json
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from store.models import Customer
from user_account.forms import CustomerRegForm
from django.contrib import messages
account_activation_token = PasswordResetTokenGenerator()

class SignInView(LoginView):
    authentication_form = CustomUserLoginForm
    template_name = 'account/registration/login.html'
        
    

class PwdResetView(PasswordResetView):
    form_class = PWDResetForm
    email_template_name = 'account/registration/password_reset_email.html'
    template_name = 'account/registration/password_reset_form.html'
    success_url = reverse_lazy('account:password_reset_done')

class PResetDoneView(PasswordResetDoneView):
    template_name = 'account/registration/password_reset_done.html'
    title = _('Password reset sent')

class PwdResetConfirmView(PasswordResetConfirmView):
    form_class = SetPWDForm
    template_name = 'account/registration/password_reset_confirm.html'
    success_url = reverse_lazy('account:password_reset_complete')
    
class PwdResetCompleteView(PasswordResetCompleteView):
    template_name = 'account/registration/password_reset_complete.html'

@method_decorator(login_required(login_url='/account/signin/'), name='dispatch')
class PwdChangeFormView(PasswordChangeView):
    form_class = PwdChangeForm
    success_url =reverse_lazy('store:home')
    template_name = 'account/user/password_change_form.html'



def signup(request):
    if request.user.is_authenticated:
        return redirect('store:home')
    else:
        form = CustomUserCreationForm()
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():

                client_key = request.POST['g-recaptcha-response']
                # print('client_key',client_key)
                secret_key = '6LcAx3UcAAAAAB6IDR3ZKLXQY2HFV92DyL6E1mxg'
                data = {
                    'secret':secret_key,
                    'response': client_key
                }
                r = requests.post(' https://www.google.com/recaptcha/api/siteverify',data=data)
                #(r)
                #()
                response = json.loads(r.text)
                #(response['success'])
                if response['success']:
                    #(form)
                    #(form.cleaned_data['email'])
                    user = form.save(commit=False)
                    user.email = form.cleaned_data['email']
                    user.set_password(form.cleaned_data['password1'])
                    user.is_active = False
                    user.save()
                    #send mail
                    current_site = get_current_site(request)
                    subject = 'Activate Your Account'
                    message = render_to_string('account/registration/account_activation_email.html',{
                    'user':user,
                    'domain':current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':account_activation_token.make_token(user)
                    })
                    #('domain',current_site.domain)
                    #()
                    #()
                    
                    user.email_user(subject=subject,message=message)
                    return render(request,'account/registration/reg_info.html')
                
                
        
        return render(request,'account/registration/signin.html',{'form':form})

def account_activate(request ,uidb64,token ):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        userobj = MyUser.objects.get(pk=uid)
        #('inside try block')
    except():
        #('inside except block')
        pass
    # user = authenticate(username = userobj.username,password=userobj.password)
    #(userobj)
    if userobj is not None and account_activation_token.check_token(userobj,token):
        #('insid user obk')
        userobj.is_active = True
        userobj.save()
        #('inside account activation')
        #(userobj.is_active)
        login(request,userobj,backend='django.contrib.auth.backends.ModelBackend')
        return redirect('store:home')
    return HttpResponse('invalid login')
        

@method_decorator(login_required(login_url='/account/signin/'), name='dispatch')
class CustomerRegView(CreateView):
    template_name = 'customer/customer_reg_form.html'
    form_class = CustomerRegForm
    success_url = reverse_lazy('cart:buy')

    def form_valid(self,form):
        cus_num = len(Customer.objects.filter(customer=self.request.user))
        #(cus_num)
        if(cus_num >3):
            messages.warning(self.request, 'Sorry you cannot register ')
            return redirect('account:profile') 
        obj = form.save(commit=False)
        obj.customer = self.request.user
        obj.save()
        return redirect('account:profile')

@method_decorator(login_required(login_url='/account/signin/'), name='dispatch')
class ProfileView(TemplateView):
    template_name = 'customer/profile.html'
    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(**kwargs)
        context['customers'] = Customer.objects.filter(customer=self.request.user)
        context['form'] = CustomerRegForm()
        return context

@method_decorator(login_required(login_url='/account/signin/'), name='dispatch')
class ProfileEditView(View):
    def get(self,request,*args,**kwargs):
        #(kwargs)
        #(kwargs.get('uuid'))
        customer = Customer.objects.get(cid=self.kwargs['uuid'],customer=self.request.user)
        form = CustomerRegForm(instance=customer)
        return render(request,'customer/profile_edit.html',{'form':form})
    def post(self,request,*args,**kwargs):
        customer = Customer.objects.get(cid=self.kwargs['uuid'],customer=self.request.user)
        form = CustomerRegForm(self.request.POST or None,instance=customer)
        if form.is_valid():
            form.save()
            return redirect('account:profile')
        return render(request,'customer/profile_edit.html',{'form':form})


        

    