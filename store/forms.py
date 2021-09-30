from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets
from .models import Product_image, ProductInventory
class SkuChecker(forms.ModelForm):
    class Meta:
        model = ProductInventory
        fields = ('product','combination_string','quantity')

        widgets = {
            'combination_string':forms.TextInput(attrs={'placeholder':'enter like x-y-z'})
        }
    def listToStr(self,val):
        emp = ''
        for c in val:
            emp+=c
        return emp 

    def clean_combination_string(self):
       
        cleaned_data = super().clean()

        combination_str = cleaned_data.get('combination_string')
        comb_str = sorted(cleaned_data.get('combination_string').lower().split('-'))

        
        if ProductInventory.objects.filter(sku=self.listToStr(comb_str)).exists():
            raise ValidationError('combination string already exists')
        return combination_str
            
    def save(self,commit=True):
        
        instance = super(SkuChecker,self).save(commit=False)
        instance.sku = self.listToStr(sorted(instance.combination_string.lower().split('-')))
        if commit:
            instance.save()
        return instance

class ImageHandler(forms.ModelForm):
    class Meta:
        model = Product_image
        fields = '__all__'
    def clean_color(self):
        cleaned_data = super().clean()
        color = cleaned_data.get('color')
        if cleaned_data.get('color'):
            return cleaned_data.get('color').title()
        return color