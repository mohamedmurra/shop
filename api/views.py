from django.shortcuts import render,redirect
from rest_framework.decorators import api_view
from rest_framework import generics ,status 
from .serializers import Product_api, shipping_serl, create_order_serl, create_orderitems, repairs_serl, Customer_ser, Register_serl
from MyStore.models import Product ,shippingAddress ,Order ,OrderItem,repairs
from users.models import CustomUser
from rest_framework.response import Response
# Create your views here.

class Product_serli(generics.ListAPIView):
 queryset = Product.objects.all()
 serializer_class =Product_api


@api_view(['POST',])
def RegistrationView(request):
  serializ = Register_serl(data=request.data)
  data  ={}
  if serializ.is_valid():
    account = serializ.save()
    data['response'] ='sucessfuly registered user'
    data['email'] =account.email
    data['username'] =account.username
  else :
    data = serializ.errors
  return Response(data)


class Customer_api(generics.UpdateAPIView):
 queryset = Product.objects.all()
 serializer_class = Customer_ser



class repairs_api(generics.CreateAPIView):
 queryset = repairs.objects.all()
 serializer_class = repairs_serl

class shipping_api(generics.CreateAPIView):
 queryset = shippingAddress.objects.all()
 serializer_class =shipping_serl

class Order_create_api(generics.CreateAPIView):
  queryset = Order.objects.all()
  serializer_class =create_order_serl


class create_orderitems_api(generics.CreateAPIView):
  queryset = OrderItem.objects.all()
  serializer_class = create_orderitems




