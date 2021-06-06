from rest_framework.serializers import ModelSerializer
from MyStore.models import Product, Order ,shippingAddress ,OrderItem ,repairs,Customer
from users.models import CustomUser
from rest_framework import serializers

class Product_api(ModelSerializer):
 class Meta:
  model =Product
  fields = '__all__'
 
 
class Register_serl(serializers.ModelSerializer):
  password2 =serializers.CharField(style={'input_type':'password2'},write_only=True)

  class Meta:
    model =CustomUser
    fields =['username','password','password2','phone_number','email']
    extra_kwargs ={
      'password':{'write_only':True}
    }
  def save(self):
    account =CustomUser(
      email=self.validated_data['email'],
      username =self.validated_data['username'],
      phone_number=self.validated_data['phone_number'],
      )
    password =self.validated_data['password']
    password2 =self.validated_data['password2']
    if password != password2:
      raise serializers.ValidationError({'password':'Password must match'})
    account.set_password(password)
    account.save()
    return account


class Customer_ser(ModelSerializer):
 class Meta:
  model = Customer
  fields = '__all__'

class repairs_serl(ModelSerializer):
 class Meta:
  model = repairs
  fields = '__all__'


class shipping_serl(ModelSerializer):
 class Meta:
  model = shippingAddress
  fields = '__all__'


class create_order_serl(ModelSerializer):
 class Meta:
  model = Order
  fields = '__all__'

class create_orderitems(ModelSerializer):

 class Meta:
  model = OrderItem
  fields = '__all__'


