from django.db import models
from users.models import CustomUser


# Create your models here.


class Catagory(models.Model):
  name = models.CharField(max_length=200)
  image = models.ImageField(upload_to='images/catagory',blank=True,null=True)

  def __str__(self):
    return self.name


class Brand(models.Model):
  name = models.CharField(max_length=200)
  image = models.ImageField(upload_to='images/brand', blank=True, null=True)

  def __str__(self):
    return self.name
  
class Customer(models.Model):
  user = models.OneToOneField(CustomUser ,on_delete=models.CASCADE ,null=True,blank=True)
  name=models.CharField(max_length=200 ,null=True)
  email = models.EmailField(unique=True)

class Product(models.Model):
  name = models.CharField(max_length=200)
  catagory = models.ForeignKey(Catagory, on_delete=models.SET_NULL,null=True)
  brand =models.ForeignKey(Brand, on_delete=models.SET_NULL,null=True)
  image = models.ImageField(upload_to='images/products')
  description = models.TextField(blank=True, null=True)
  price =models.DecimalField(max_digits=10 ,decimal_places=2)
  aviable =models.BooleanField(default=False)
  stack = models.IntegerField(default=0)
  tags = models.CharField(max_length=100,unique=True ,blank=True ,null ='True')
  color =models.CharField(max_length=50,blank=True ,null=True)
  size = models.CharField(max_length=50,blank=True,null=True)
  digital =models.BooleanField(default=False,null=True ,blank=False)

  def __str__(self):
      return self.name

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
  tansaction_id =models.CharField(max_length=10,unique=True)

  def __str__(self):
      return str(self.id)
    
  @property
  def shipping(self):
    shipping = False
    orderitems = self.orderitem_set.all()
    for i in orderitems:
      if i.product.digital == False:
        shipping = True
    return shipping

  @property
  def get_cart_total(self):
    orderitems= self.orderitem_set.all()
    total = sum([item.get_total for item in orderitems])
    return total

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
    total =self.product.price * self.quantity
    return total

class shippingAddress(models.Model):
  name =models.ForeignKey(Customer ,on_delete=models.SET_NULL ,null=True)
  location_url =models.URLField()
  order =models.ForeignKey(Order, on_delete=models.SET_NULL ,null=True)
  address =models.CharField(max_length=100)
  area =models.CharField(max_length=100)
  street =models.CharField(max_length=100)
  building =models.CharField(max_length=100)
  city =models.CharField(max_length=100)
  detail =models.TextField(blank=True,null=True)

  def __str__(self):
      return self.address

class repairs(models.Model):
  image =models.ImageField(upload_to='images/Sim_card')
  info =models.TextField()

class sim_config(models.Model):
  image1 = models.ImageField(upload_to='sim_config')
  image2 = models.ImageField(upload_to='sim_config')


  
