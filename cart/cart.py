from store.models import Product_image
from store.models import Product
from django.http import JsonResponse
import json

class Cart():
    def __init__(self,request):
        self.request = request
        
        
    def add_to_cart(self,request,**kwargs):
        #('#################&&&&&&&')
        cart_products = request.session.get('cart')
        
        if cart_products is not None:
            img = None
            if kwargs['id'] not in cart_products.keys():
                extra_info = json.loads(kwargs['extra_info'])
                product_obj = Product.objects.get(id = kwargs['id'])
                if 'Color' in extra_info.keys():
                    try:
                        img = Product_image.objects.filter(product=product_obj, color=extra_info['Color']).first().id
                    except:
                        img = None
                cart_products[kwargs['id']] = {'price':kwargs['price'],'quantity':kwargs['quantity'],'extra_info':extra_info,'img':img}
                request.session['cart'] = cart_products
                request.session.modified = True
            else:
                #('hello')
                request.session['cart'][kwargs['id']]['quantity'] = kwargs['quantity']
                request.session['cart'] = request.session.get('cart')
                request.session.modified = True
                return JsonResponse({'msg':'successfully updated'})
        else:
            img = None
            extra_info = json.loads(kwargs['extra_info'])
            product_obj = Product.objects.get(id = kwargs['id'])
            if 'Color' in extra_info.keys():
                try:
                    img = Product_image.objects.filter(product=product_obj, color=extra_info['Color']).first().id
                except:
                    img = None

            request.session['cart'] = {kwargs['id']:{'price':kwargs['price'],'quantity':kwargs['quantity'],'extra_info':extra_info,'img':img}}
            request.session['shipping_charge'] = 300
            request.session.modified = True
            


    def show_quantity(self):
        
        sum = 0
        item = self.request.session.get('cart')
        # #(item)
        if item:
            for x in item.keys():
                sum = sum + int(item[x]['quantity'] )
                # #(sum)
            return sum
                
        return 0

    def show_items(self):
        quantity = []
        products = Product.objects.filter(id__in=self.request.session.get('cart').keys())
        for p in products:
            subtotal = int(self.request.session.get('cart')[str(p.id)]['quantity'])*p.discount_price
            # #(subtotal)
            # #(p.id)
            try:
                if self.request.session.get('cart')[str(p.id)]['img']:
                    quantity.append({'product':p,'quantity':self.request.session.get('cart')[str(p.id)]['quantity'],'subtotal':subtotal,'extra_info':self.request.session.get('cart')[str(p.id)]['extra_info'],'img':Product_image.objects.get(id = self.request.session.get('cart')[str(p.id)]['img'])})
                else:
                    quantity.append({'product':p,'quantity':self.request.session.get('cart')[str(p.id)]['quantity'],'subtotal':subtotal,'extra_info':self.request.session.get('cart')[str(p.id)]['extra_info'],'img':None})

            except:
                quantity.append({'product':p,'quantity':self.request.session.get('cart')[str(p.id)]['quantity'],'subtotal':subtotal})

        # #('quantity',quantity)
        return(quantity)

    def subTotal(self):
        #return price excluding shipping address
        sum = 0
        products = self.show_items()
        for p in products:
            sum = sum + int(p['subtotal'])
            #sum = sum + self.request.session.get('shipping_charge')
        return sum

    def showShippingCharge(self):
        return self.request.session.get('shipping_charge')

    def total(self):
        #returns the total charge including shipping charge
        return self.subTotal()+self.showShippingCharge()
    

        