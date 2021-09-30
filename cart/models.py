from store.models import Product_image
from django.db.models.deletion import SET_NULL
from user_account.models import MyUser
from django.db import models
from store.models import Customer,Product
import json
from jsonfield import JSONField
from store.models import Product

class Order(models.Model):
    order_status = (
        
        ('Accepted','Accepted'),
        ('Packed','Packed'),
        ('On The Way','On The Way'),
        ('Delivered','Delivered'),
        ('Reject','Reject')
    )
    user = models.ForeignKey(MyUser,on_delete=SET_NULL,null=True)
    order_id = models.CharField(max_length=50)
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,related_name='orders')
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField()
    price = models.FloatField()
    variation = JSONField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10,choices=order_status,null=True)

    def __str__(self):
        return f"{self.product.title}-{self.variation}"
    class Meta:
        ordering = ['-created_at']

    def show_img(self):
        print('show img called')
        try:
            product_obj = Product.objects.get(id = self.product.id)
            if self.variation:
                if 'Color' in self.variation.keys():
                    try:
                        return Product_image.objects.filter(product=product_obj,color=self.variation['Color']).first().image.url
                    except:
                        return None
            try:
                return Product_image.objects.get(product=product_obj,is_featured=True).image.url
            except:
                try:
                    return Product_image.objects.filter(product=product_obj).first().image.url
                except:
                    return None
        except:
            return None


        # else:
        #     try:
        #         return Product_image.objects.get(product=product_obj,is_featured=True).image.url
        #     except:
        #         try:
        #             return Product_image.objects.filter(product=product_obj).first().image.url
        #         except:
        #             return None
        
        
        

       

   
            


