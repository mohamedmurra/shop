from django.forms import ModelForm
from .models import Product, Brand, Catagory, repairs,shippingAddress,sim_config

class product_form(ModelForm):
  
 class  Meta:
  model = Product
  fields ='__all__'

class brand_form(ModelForm):
 class  Meta:
  model = Brand
  fields ='__all__'


class sim_confi_form(ModelForm):
 class Meta:
  model = sim_config
  fields = '__all__'

class shipping_form(ModelForm):
 class Meta:
  model = shippingAddress
  fields = '__all__'

class catagory_form(ModelForm):
 class  Meta:
  model = Catagory
  fields ='__all__'

class repairs_form(ModelForm):
 class  Meta:
  model = repairs
  fields ='__all__'
