from django.http.response import HttpResponse, JsonResponse,HttpResponseRedirect
from django.shortcuts import redirect, render,get_object_or_404
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from .models import Catagory, Product, Product_image, ProductInventory, ProductVariationsOptions, SubCatagory
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView
import json
from django.core.mail import send_mail
from cart.cart import Cart
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Avg
def Home(request):
    query_set = {}
    catagories = Catagory.objects.all()
    for c in catagories:
        if c.cat_prods():
            query_set[c] = c.cat_prods()[:min(len(c.cat_prods()),5)]
   
    x=ProductInventory.objects.filter(sku = '12888blacknoteredmi')
    
    return render(request,"store/home.html",{'query_set':query_set,'session':request.session.get('cart')})
    
class ProductSearchView(View):
    def get(self,request,*args,**kwargs):

        # print(request.GET.get('search'))
        prods = Product.objects.filter(title__icontains = request.GET.get('search'),is_stock=True)
        paginator = Paginator(prods.order_by('id'),20)
        if request.GET.get('price'):
            if request.GET.get('price') == 'Low-to-High':
                # print(prods.order_by('discount_price'))
                paginator = Paginator(prods.order_by('discount_price'),20)
            else:
                paginator = Paginator(prods.order_by('-discount_price'),20)
        page_obj = paginator.get_page(request.GET.get('page'))
        return render(request,'store/product_search.html',{'page_obj':page_obj})


class ProductDetailView(TemplateView):
    template_name = 'store/product_detail_view.html'

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']
        context['prod'] = get_object_or_404(Product,slug=slug)
        context['length'] = len(context['prod'].productvariationsoptions_set.all())
        if self.request.session.get('cart'):
            context['cart_keys'] = [ int(x) for x in self.request.session.get('cart').keys()]
        return context

class CatagoryView(View):
    template_name = 'store/catagory.html'
    
    def get(self,request,*args,**kwargs):
        
        cat_name = get_object_or_404(Catagory,slug=kwargs['slug'])

        paginator = Paginator(cat_name.cat_prods().order_by('id'),20)
        page_obj = paginator.get_page(request.GET.get('page'))
        return render(request,'store/catagory.html',{'page_obj':page_obj,'subcatagory':cat_name.subcatagory_set.all()})
        
class ProductListView(View):
    def get(self,request,*args,**kwargs):
        # print(request.GET.get('page'))
        # print(request.GET.get('price'))
        sub_cat = get_object_or_404(SubCatagory,slug=kwargs['slug'])
        paginator = Paginator(sub_cat.sub_cat_prods().order_by('id'),20)
        if request.GET.get('price'):
            if request.GET.get('price') == 'Low-to-High':
                paginator = Paginator(sub_cat.sub_cat_prods().order_by('discount_price'),20)
            else:
                paginator = Paginator(sub_cat.sub_cat_prods().order_by('-discount_price'),20)
        page_obj = paginator.get_page(request.GET.get('page'))
        return render(request,'store/product_list_view.html',{'page_obj':page_obj})

