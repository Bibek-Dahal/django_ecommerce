from django.db import models
from autoslug import AutoSlugField
from django.forms.fields import UUIDField
from django.urls import reverse
from user_account.models import MyUser
from django.utils import timezone
from cloudinary.models import CloudinaryField
from .product_model_manager import ProductManager
import uuid
from django.utils.translation import ugettext_lazy as _
from ckeditor.fields import RichTextField


class Customer(models.Model):
    cid = models.UUIDField(default=uuid.uuid4,editable=False)
    customer = models.ForeignKey(MyUser,on_delete=models.CASCADE,related_name='customer')
    full_name = models.CharField(max_length=100,unique=True)
    phone_number = models.CharField(max_length=10)
    temporary_address = models.CharField(max_length=100,blank=True)
    shipping_address = models.CharField(max_length=100)
    date_joined = models.DateTimeField(default= timezone.now)

    def __str__(self):
        return self.full_name

class Catagory(models.Model):
    name = models.CharField(max_length = 80,unique= True)
    slug = AutoSlugField(populate_from = 'name',unique=True)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-id']
   

    def get_absolute_url(self):
        return reverse('store:catagory_detail',args = [self.slug])
    
    def cat_prods(self):
        return self.products.all().filter(is_stock=True)

class SubCatagory(models.Model):
    catagory = models.ForeignKey(Catagory,on_delete=models.CASCADE)
    name = models.CharField(max_length=100,unique=True)
    slug = AutoSlugField(populate_from = 'name',unique=True)

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('store:products',args = [self.slug])

    def sub_cat_prods(self):
        return self.product_set.all().filter(is_stock=True)
    
class Product(models.Model):
    catagory = models.ForeignKey(Catagory,on_delete= models.CASCADE,related_name = 'products')
    subcatagory = models.ForeignKey(SubCatagory,on_delete=models.CASCADE,default='')
    title = models.CharField(max_length=100,unique = True)
    description = RichTextField(blank=True,null=True)
    marked_price = models.FloatField()
    discount_price = models.FloatField()
    slug =AutoSlugField(populate_from = 'title',unique=True)
    is_stock = models.BooleanField(default = True)
    objects = models.Manager()
    prods = ProductManager()
    
    def Description(self):
        return self.description[:20]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('store:product_detail',args = [self.slug])

    class Meta:
        ordering = ['-id']
    
    def show_img(self):
        try:
            return Product_image.objects.get(product=self,is_featured=True).image.url
        except:
            try:
                return Product_image.objects.filter(product=self).first().image.url
            except:
                return None

class ProductVariationsOptions(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.product.title}-{self.name}"
    class Meta:
        ordering = ['-id']

    # class Meta:
    #     verbose_name = _('product variation option')
    #     verbose_name_plural = _('product variations options')
   
class ProductVariationValue(models.Model):
    product_variation_option = models.ForeignKey(ProductVariationsOptions,on_delete=models.CASCADE)
    product_variation_value = models.CharField(max_length=100)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.product_variation_option.product.title}-{self.product_variation_option.name}-{self.product_variation_value}"

    def show_first_img(self):
        try:
            return self.product_image.all().first()
        except:
            return None

class ProductInventory(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    combination_string = models.CharField(max_length=150,unique=True)
    sku = models.CharField(max_length=150)
    quantity = models.PositiveIntegerField(default=0)

    # @property
    # def sku(self):
    #     comb_str = sorted(self.combination_string.lower().split('-'))

    #     def listToStr():
    #         emp = ''
    #         for c in comb_str:
    #             emp+=c
    #         # self.sku = emp
    #         # self.save()
    #         return emp
        
    #     return(listToStr())


    class Meta:
        verbose_name = _('product inventory')
        verbose_name_plural = _('product inventories')

class Product_image(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name = "product_image")
    image = CloudinaryField('product/image')
    color = models.CharField(max_length=40,blank=True,null=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



# class Order(models.Model):
#     customer = models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='orders')
#     cart_product = models.ManyToManyField(Cart,related_name='orders')


    


