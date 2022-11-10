from unicodedata import name
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_save
import random
import string
from cloudinary.models import CloudinaryField
from Coupon.models import Coupons
from PIL import Image
from decimal import Decimal

# Create your models here.

def uplaod_lucation(instance, filename):
  file_path = 'Product/{catagory}/{name}-{filename}'.format(
     catagory=str(instance.catagory), name=str(instance.name), filename=filename)
  return file_path

def product_lucation(instance, filename):
  file_path = 'Product/Catagory/{name}/{name}-{filename}'.format(
     name=str(instance.name),  filename=filename)
  return file_path


def Brand_lucation(instance, filename):
  file_path = 'Product/Catagory/{name}/{name}-{filename}'.format(
      name=str(instance.name),  filename=filename)
  return file_path

def TESTIMONIALS_lucation(instance, filename):
  file_path = 'TESTIMONIALS/-{filename}'.format(
      name=str(instance.name),  filename=filename)
  return file_path


class Brand(models.Model):
  name = models.CharField(max_length=100)
  image = CloudinaryField('image')
  slug = models.SlugField(unique=True)
  note =models.TextField(blank=True,null=True)

  def __str__(self):
    return self.name

class TESTIMONIALS(models.Model):
  name = models.CharField(max_length=100)
  image = CloudinaryField('image')
  note =models.TextField(blank=True,null=True)
  created =models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.name


class Tags(models.Model):
  name = models.CharField(max_length=100)
  slug = models.SlugField(unique=True)

  def __str__(self):
    return self.name

class Catagory(models.Model):
  name = models.CharField(max_length=200,unique=True)
  image = CloudinaryField('image')
  slug =models.SlugField(unique=True ,blank=True,null=True)

  def __str__(self):
    return self.name
  



  
class Customer(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True,blank=True)

  def __str__(self):
    return self.user.email


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def post_save_reciver(sender, instance, created,*args, **kwargs):
 if created:
  Customer.objects.create(user=instance, id=instance.id)


class Product(models.Model):
  name = models.CharField(max_length=200, blank=False, null=False)
  catagory = models.ForeignKey(Catagory, on_delete=models.SET_NULL, null=True)
  image = CloudinaryField('image')
  discount =models.IntegerField(blank=True,null=True)
  description = models.TextField(blank=True, null=True)
  price =models.IntegerField(blank=True, null=True)
  brand =models.ForeignKey(Brand,on_delete=models.SET_NULL,blank=True,null=True)
  aviable =models.BooleanField(default=False)
  stack = models.IntegerField(default=0)
  slug = models.SlugField(unique=True,blank=True )
  tags = models.ManyToManyField(Tags,related_name='tags',blank=True)
  created =models.DateTimeField(auto_now_add=True)

  def __str__(self):
      return self.name

  def has_stack(self):
    return self.stack >= 0

  @property
  def new_price(self):
    if self.discount:
      return self.price - self.discount
    else:
      return self.price
     

@receiver(pre_save, sender=Product)
def pre_save_reciver(sender,instance,*args,**kwargs):
 if not instance.slug:
  instance.slug = slugify(instance.name + "-" + instance.catagory.name)


@receiver(pre_save, sender=Catagory)
def pre_reciver(sender, instance, *args, **kwargs):
 if not instance.slug:
  instance.slug = slugify(instance.name + "-" + instance.image.name)



def tansaction_id_genrater():
  length =10
  while True:
    code =''.join(random.choices(string.ascii_uppercase,k=length))
    if Order.objects.filter(tansaction_id=code).count() ==0:
      break
  return code
class Order(models.Model):
  customer =models.ForeignKey(Customer, on_delete =models.SET_NULL ,null=True)
  date_orderd =models.DateTimeField(auto_now_add=True)
  ORDER_CHOICES =(
    ('Created',' Created'),
    ('Paid',' Paid'),
    ('Pinding',' Pinding'),
    ('Shipped', ' Shipped'),
    ('Refunded', ' Refunded'),
    )
  status = models.CharField(max_length=20, choices=ORDER_CHOICES ,default='Created')
  complete =models.BooleanField(default=False)
  tansaction_id =models.CharField(max_length=10,unique=True,default=tansaction_id_genrater)
  coupon =models.ForeignKey(Coupons,on_delete =models.SET_NULL ,null=True,blank=True)

  def __str__(self):
      return f'{self.tansaction_id}'
    
  @property
  def get_cart_total(self):
    orderitems= self.orderitem_set.all()
    total = sum([item.get_total for item in orderitems])
    return total

  @property
  def get_discount(self):
    if self.coupon:
      return (self.coupon.discount / Decimal(100)) * self.get_cart_total
    return Decimal(0)
  @property
  def get_cart_total_after_discount(self):
    return self.get_cart_total - self.get_discount

  @property
  def get_cart_items(self):
    orderitems= self.orderitem_set.all()
    total = sum([item.quantity for item in orderitems])
    return total

  
class OrderItem(models.Model):
  product =models.ForeignKey(Product ,on_delete=models.SET_NULL, null=True)
  order =models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
  quantity =models.IntegerField(default=0, null=True, blank=True)
  date_added =models.DateTimeField(auto_now_add=True)

  
  @property
  def get_total(self):
    if self.product.discount:
      price = self.product.price - self.product.discount
      total =price * self.quantity
      return total
    else:
      total = self.product.price * self.quantity
    return total


class shippingAddress(models.Model):
  name =models.ForeignKey(Customer ,on_delete=models.SET_NULL ,null=True)
  order =models.ForeignKey(Order, on_delete=models.SET_NULL ,null=True)
  phone_number =models.CharField(max_length=50)
  address =models.CharField(max_length=100)
  city =models.CharField(max_length=100)
  state =models.CharField(max_length=100)
  aria = models.CharField(max_length=100)
  

  def __str__(self):
      return self.address


class Review(models.Model):
  title =models.CharField(max_length=100,blank=True,null=True)
  product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
  user = models.ForeignKey(Customer, on_delete=models.CASCADE)
  body = models.TextField(blank=True, null=True)
  created = models.DateTimeField(auto_now_add=True)
  parent = models.ForeignKey(
      'Review', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)
  class Meta:
    ordering = ('created',)

  def __str__(self):
    return 'comment by {}'.format(self.user)

class WhishList(models.Model):
  customer = models.ForeignKey(
      Customer, on_delete=models.CASCADE, null=True, blank=True)
  product =models.ForeignKey(Product, on_delete=models.SET_NULL,null=True,blank=True)

  def __str__(self):
    return self.product.name

class Subscriber(models.Model):
  email =models.EmailField(unique=True,null=True)
  date =models.DateTimeField(auto_now_add=True)

  def __str__(self):
      return self.email
  

class MailMsg(models.Model):
  title =models.CharField(max_length=100)
  message = models.TextField()

  def __str__(self):
    return self.title

class Supplier(models.Model):
  name =models.CharField(max_length=100)
  email =models.EmailField()
  company_name =models.CharField(max_length=100)
  phone_number =models.IntegerField()
  address =models.TextField()

  def __str__(self):
    return self.name

class Wherehouse(models.Model):
  name =models.CharField(max_length=100)
  lucation =models.TextField(null=True,blank=True)

  def __str__(self) :
      return self.name
  

class Expense(models.Model):
  code =models.CharField(max_length=10,unique=True)
  name =models.CharField(max_length=100)
  amount =models.IntegerField()
  date =models.DateTimeField(auto_now_add=True)
  note =models.TextField(blank=True, null=True)
  wherehouse =models.ForeignKey(Wherehouse,on_delete=models.SET_NULL ,null=True,blank=True)


  def __str__(self):
    return self.name
  

class Transfere(models.Model):
  STATUS_CHOICES =(
    ('full',' full'),
    ('empty',' empty'),
    ('Partial	',' Partial	'),
    ('Pending', ' Pending'),
    )
  code = models.CharField(max_length=10,unique=True,default=tansaction_id_genrater)
  take_from =models.ForeignKey(Wherehouse,on_delete=models.CASCADE,related_name='lucation_from')
  give_to =models.ForeignKey(Wherehouse,on_delete=models.CASCADE,related_name='lucation_to')
  product =models.ForeignKey(Product,on_delete=models.CASCADE)
  date =models.DateTimeField(auto_now_add=True)
  stack =models.IntegerField(default=0)
  shupping_charge =models.IntegerField(null=True,blank=True)
  status =models.CharField(max_length=20,choices=STATUS_CHOICES,default='Partial')
  note = models.TextField(blank=True,null=True)

  def __str__(self):
    return f'taken form {self.take_from} to {self.give_to}'

  @property
  def totall_product_price(self):
    totall =self.product.price * self.stack
    if self.shupping_charge :
      totall= totall-self.shupping_charge
    return totall

  @property
  def product_new_stack(self):
    totall= self.product.stack + self.stack
    return totall

class suplier(models.Model):
  name =models.CharField(max_length=100)
  phone =models.CharField(max_length=100)
  Company =models.CharField(max_length=100)
  image = CloudinaryField('image')
  email =models.EmailField()
  address =models.TextField()

  def __str__(self):
    return self.name

class Purchase(models.Model):
  STATUS_CHOICES =(
    ('recived',' recived'),
    ('Conseld',' Conseld'),
    ('Partial	',' Partial	'),
    ('Pending', ' Pending'),
    )
  product =models.ForeignKey(Product,on_delete=models.CASCADE)
  price =models.IntegerField()
  Shupping_Cost =models.IntegerField()
  Document =models.FileField(upload_to='product/files',blank=True,null=True)
  wherehouse =models.ForeignKey(Wherehouse ,on_delete=models.CASCADE)
  stack =models.IntegerField()
  suplier =models.ForeignKey(suplier,on_delete=models.CASCADE)
  discount =models.IntegerField(blank=True,null=True)
  status =models.CharField(max_length=20,choices=STATUS_CHOICES,default='Partial')
  tax =models.IntegerField(blank=True,null=True)
  added =models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'purchase {self.stack}  of  {self.product}'

