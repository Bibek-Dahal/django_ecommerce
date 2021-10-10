from django.http import response,HttpResponseRedirect
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views.generic.base import TemplateView, View
import json
from django.conf import settings
from store.models import Product_image
from .cart import Cart
from store.models import Product, Customer
import requests
from .models import Order
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.core.mail import send_mail
import uuid
x = 0


class FailuereOrderView(View):
    def get(self,request):
        response = HttpResponseRedirect('/')
        messages.info(request, 'Sorry, Your Order Could Not Be Placed. Thank You!')
        response.delete_cookie('order')
        return response
        
class AddToCartView(View):
    def post(self, request, *args, **kwargs):
        ##('args', args)
        ##('kwargs', kwargs)
        ##(request.POST.get('quantity'))
        quantity = request.POST.get('quantity')
        cart_obj = Cart(request)
        cart_obj.add_to_cart(request, id=request.POST.get(
            'id'), quantity=request.POST.get('quantity'), price=request.POST.get('price'),extra_info = request.POST.get('extra_info'))
        items = cart_obj.show_items()
        # current_obj = Product.objects.get(id=request.POST.get('id'))
        current_obj =  get_object_or_404(Product,id=request.POST.get('id'))
        obj = [p for p in items if p['product'] == current_obj]
        ##(obj)
        ##(request.POST.get('quantity'))
        ##(cart_obj.subTotal())
        # ##(request.session.get('cart'))

        return JsonResponse({'quantity':quantity,'data': obj[0]['subtotal'],'length':cart_obj.show_quantity(), 's_price': cart_obj.subTotal(), 'length': cart_obj.show_quantity(), 'total_charge': cart_obj.total(), 'shipping_charge': cart_obj.showShippingCharge()})


@method_decorator(login_required(login_url='/account/signin/'), name='dispatch')
class CartDetailView(TemplateView):
    template_name = 'cart/cart_detail.html'

    def get_context_data(self, *args, **kwargs):
        ##('args', args)
        ##('kwargs', kwargs)
        if self.request.session.get('cart'):
            ##(self.request.session.get('cart'))
            context = super().get_context_data(**kwargs)
            cart_obj = Cart(self.request)
            ##(cart_obj.show_items())
            ##()
            ##(cart_obj.subTotal())
            context['sub_total'] = int(cart_obj.subTotal())
            context['products'] = cart_obj.show_items()
            context['length'] = cart_obj.show_quantity()
            context['shipping_charge'] = cart_obj.showShippingCharge()
            
            context['total'] = cart_obj.total()

            return context
        context = super().get_context_data(**kwargs)
        return context


@method_decorator(login_required(login_url='/account/signin/'), name='dispatch')
class RemoveCartView(View):

    def post(self, request, *args, **kwargs):
        cart_obj = Cart(self.request)
        ##('args', args)
        ##('kwargs', kwargs)
        ##(request.POST.get('pk'))
        pk = request.POST.get('pk')
        ##(request.session.get('cart'))
        items = request.session.get('cart')
        items.pop(request.POST.get('pk'))
        request.session['cart'] = items
        request.session.modefied = True
        # request.session.clear_expired()

        return JsonResponse({'id':pk, 's_price': cart_obj.subTotal(), 'length': cart_obj.show_quantity(), 'total_charge': cart_obj.total(), 'shipping_charge': cart_obj.showShippingCharge()})


class VerifyKhalthiView(View):
    def post(self, request, *args, **kwargs):
        ##(self.request.POST.get('token'))
        ##(self.request.POST.get('amount'))
        # ##('data: ', request.POST.get('token'))
        # ##('amount',request.POST.get('amount'))
        token = self.request.POST.get('token')
        amount = self.request.POST.get('amount')
        # ##('amount', request.POST.get('name[amount]'))
        # ##(token)

        url = "https://khalti.com/api/v2/payment/verify/"
        payload = {
            "token": token,
            "amount": amount
        }
        headers = {
            "Authorization": settings.KHALTHI_SECRET_KEY
        }

        response = requests.post(url, payload, headers=headers)
        # res = [r for r in response]
        ##(response)
        ##(response.text)
        ##(json.loads(response.text))
        res = json.loads(response.text)
        # ##('response', response)
        # ##()
        # ##()
        # ##(res.get('idx'))
        if res.get('idx'):
            return JsonResponse({'msg': 'success'})
        else:
            return JsonResponse({'msg':'failed'})


      

order_id = None
@method_decorator(login_required(login_url='/account/signin/'), name='dispatch')
class BuyProducts(View):
    def generate_uuid(self):
            return(uuid.uuid4())

    def get(self, request):
        cart_obj = Cart(request)
        customer = Customer.objects.filter(customer=request.user)
        

        if customer:
            if request.session.get('cart'):
                order = self.request.COOKIES.get('order')
                ##('order',order)
                if order == None:
                    order = self.generate_uuid()
                    ##(order)
                context = {
                    'products': cart_obj.show_items(),
                    'total': cart_obj.subTotal(),
                    'customers': Customer.objects.filter(customer=self.request.user),
                    'uuid':order
                }
                response =  render(request, 'cart/checkout.html', context)
                response.set_cookie('order',order)
                return response
            else:
                return render(request, 'cart/add_to_cart_info.html')
        else:
            return redirect('account:customer_reg')

class VerifyEsewa(View):
    def get(self,request):
        url ="https://uat.esewa.com.np/epay/transrec"
        d = {
            'amt': 100,
            'scd': settings.ESEWA_SECRET_KEY,
            'rid': request.GET.get('refId'),
            'pid':request.GET.get('oid'),
        }
        resp = requests.post(url, d)
        if resp.status_code == 200:
            id = request.GET.get('cid')
            order_id = request.GET.get('oid')
            ##(order_id)
            cart_obj = Cart(request)
            user = request.user
            customer = Customer.objects.get(id=id)
        
            products = cart_obj.show_items()
            for p in products:
                def checkEmpty():
                    if p['extra_info']:
                        return p['extra_info']
                    else:
                        return None
                Order.objects.create(user=user, customer=customer,order_id=order_id,product=p['product'], quantity=p['quantity'],price=p['subtotal'],variation=checkEmpty())
                
            del request.session['cart']
            response = HttpResponseRedirect('/')
            # response.delete_cookie['order']
            messages.info(request, 'Your Order Has Been Successfully Placed.')
            response.delete_cookie('order')
            ##(user.email)
            return response
        else:
            response = HttpResponseRedirect('/')
            messages.info(request, 'Sorry, Your Order Could Not Be Placed. Thank You!')
            response.delete_cookie('order')
            return response
        

        

@method_decorator(login_required(login_url='/account/signin/'), name='dispatch')
class OrderView(View):
    def post(self, request):
        order_id = request.POST.get('order')
        ##(order_id)
        cart_obj = Cart(request)
        user = request.user
        # customer = Customer.objects.get(id=request.POST.get('id'))
        customer = get_object_or_404(Customer,id=request.POST.get('id'))
        ##('inside order')
        ##(cart_obj.show_items())
        ##(request.POST.get('id'))
        products = cart_obj.show_items()
        for p in products:
            def checkEmpty():
                if p['extra_info']:
                    return p['extra_info']
                else:
                    return None
            Order.objects.create(user=user, customer=customer,order_id=order_id,
                                 product=p['product'], quantity=p['quantity'],price=p['subtotal'],variation=checkEmpty())
            
        del request.session['cart']
        response = HttpResponseRedirect('/')
        messages.info(request, 'Your Order Has Been Successfully Placed.')
        response.delete_cookie('order')
        ##(user.email)
        return response


@method_decorator(login_required(login_url='/account/signin/'), name='dispatch')
class MyOrderView(TemplateView):
    template_name = 'cart/my_order.html'
    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data()
        context['orders']  = Order.objects.filter(user=self.request.user)
        return context

class DispImg(View):
    def get(self,request):
        if self.request.is_ajax:
            product_id = request.GET.get('product')
            color = request.GET.get('color')
            