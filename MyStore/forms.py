from django.forms import ModelForm
from  django import forms
from account.models import Acount
from Coupon.models import Coupons
from django.contrib.auth.forms import UserCreationForm ,authenticate
from .models import Product, Catagory, Wherehouse, shippingAddress, Customer, Review, TESTIMONIALS, Subscriber,Brand,Order,Wherehouse,Expense,Transfere,suplier,Purchase



class Purchase_form(forms.ModelForm):
  class Meta:
    model = Purchase
    fields ='__all__'
class Expense_form(forms.ModelForm):
  class Meta:
    model = Expense
    fields =('name','code','amount','note','wherehouse')

class TESTO_form(forms.ModelForm):
  class Meta:
    model = TESTIMONIALS
    fields ='__all__'
class Suplier_form(forms.ModelForm):
  class Meta:
    model = suplier
    fields ='__all__'
class coupon_update_form(forms.ModelForm):
  class Meta:
    model = Coupons
    fields ='__all__'
class subscrbe_form(forms.ModelForm):
  class Meta:
    model = Subscriber
    fields = ('email', )
class searsh_form(forms.ModelForm):
  items = forms.CharField()
class ReviewForm(forms.ModelForm):
  user = Customer.user
  class Meta:
    model = Review
    fields = ('body','title')
class product_form(forms.ModelForm):
 class  Meta:
  model = Product
  fields = ('name', 'catagory', 'price', 'discount',
            'aviable', 'stack', 'brand', 'slug', 'description', 'image',)

  widgets={
      'name': forms.TextInput(attrs={'class': 'col-md-6 form-control round bg-transparent text-dark'}),
      'price': forms.TextInput(attrs={'class': 'col-md-6 form-control round bg-transparent text-dark'}),
      'discount': forms.TextInput(attrs={'class': 'col-md-6 form-control round bg-transparent text-dark'}),
      'stack': forms.TextInput(attrs={'class': 'col-md-6 form-control round bg-transparent text-dark'}),
      'slug': forms.TextInput(attrs={'class': 'col-md-6 form-control round bg-transparent text-dark'}),
      'description': forms.Textarea(attrs={'class': 'col-md-12 form-control round bg-transparent text-dark'}),
      'image': forms.FileInput(attrs={'class': 'col-md-12 form-control round bg-transparent text-dark'}),
  }
class catagory_form(forms.ModelForm):
 class  Meta:
  model = Catagory
  fields ='__all__'

class brand_form(forms.ModelForm):
  class Meta:
    model = Brand
    fields ='__all__'
class register_form(UserCreationForm):
 email = forms.EmailField(max_length=50, help_text='User must have email')

 class Meta:
  model = Acount
  fields = ('email', 'username', 'password1', 'password2',)
class AuthenticationForm(forms.ModelForm):
 password = forms.CharField(label='password', widget=forms.PasswordInput)

 class Meta:
  model = Acount
  fields = ('email', 'password')

 def clean(self):
  if self.is_valid():
   email = self.cleaned_data['email']
   password = self.cleaned_data['password']
   if not authenticate(email=email, password=password):
    raise forms.ValidationError('Invalid login')
class UserUpdateForm(forms.ModelForm):
  class Meta:
    model = Acount
    fields = ('email', 'username', 'image','phone_number','first_name','last_name','gender')

  def clean_email(self):
    if self.is_valid():
      email = self.cleaned_data['email']
      try:
        account = Acount.objects.exclude(
            pk=self.instance.pk).get(email='email')
      except Acount.DoesNotExist:
        return email
      raise forms.ValidationError(f'{email} is alredy in use')

  def clean_username(self):
    if self.is_valid():
      username = self.cleaned_data['username']
      try:
        account = Acount.objects.exclude(
            pk=self.instance.pk).get(username='username')
      except Acount.DoesNotExist:
        return username
      raise forms.ValidationError(f'{username} is alredy in use')

  def clean_username(self):
    if self.is_valid():
      username = self.cleaned_data['username']
      try:
        account = Acount.objects.exclude(
            pk=self.instance.pk).get(username='username')
      except Acount.DoesNotExist:
        return username
      raise forms.ValidationError(f'{username} is alredy in use')
class CustomerUpdateForm(forms.ModelForm):
  class Meta:
    model = Customer
    fields = '__all__'

class Contact_form(forms.Form):
  subject = forms.CharField(max_length=100)
  email =forms.EmailField(max_length=50)
  message = forms.CharField(widget=forms.Textarea,max_length=2000)

class order_update_form(forms.ModelForm):
  class Meta:
    model = Order
    fields = ('status', 'complete')

class Shipping_form(forms.ModelForm):
  class Meta:
    model = shippingAddress
    fields =('phone_number','address','city','state','aria')

class wherehouse_form(forms.ModelForm):
  class Meta:
    model = Wherehouse
    fields ='__all__'

class Transfere_form(forms.ModelForm):
  class Meta:
    model = Transfere
    fields =('code','take_from','give_to','status','product','stack','shupping_charge','note')