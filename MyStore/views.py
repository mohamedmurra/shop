from django.shortcuts import render ,redirect
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate ,login ,logout
from codes.forms import CodeForm ,Creation_form
from users.models import CustomUser 
import requests as rq
from .models import Product , Catagory ,Brand ,Order ,OrderItem ,repairs ,shippingAddress,Customer
from django.http import JsonResponse
import json
from .forms import product_form ,brand_form,catagory_form,repairs_form,sim_confi_form
from .decrators import allowed_user
import datetime

# Create your views here.
@login_required()
def add_product(request):
   form =product_form()
   if request.method == 'POST': 
      form =product_form(request.POST, request.FILES)
      if form.is_valid():
         form.save()
         return redirect('store')
 
   return render(request ,'add_product.html',{'form':form})



@login_required()
@allowed_user(allowed_roles=['Admin'])
def add_brand(request):
   form =brand_form()
   if request.method == 'POST': 
      form =brand_form(request.POST, request.FILES)
      if form.is_valid():
         form.save()
         return redirect('store')
   return render(request ,'add_brand.html',{'form':form})

@login_required()
@allowed_user(allowed_roles=['Admin'])
def add_catagory(request):
   form =catagory_form()
   if request.method == 'POST': 
      form =catagory_form(request.POST, request.FILES)
      if form.is_valid():
         form.save()
         return redirect('store')
   return render(request ,'add_catagory.html',{'form':form})


def store(request):
   if request.user.is_authenticated:
      customer =request.user.customer
      order ,created = Order.objects.get_or_create(customer=customer ,complete=False)
      items =order.orderitem_set.all()
   else:
      items =[]
      order ={'get_cart_total':0,'get_cart_items':0,'shipping':False}
      cartitem =order['get_cart_items']
   return render(request ,'store.html',{'products':Product.objects.all})

def cart(request):
   if request.user.is_authenticated:
      customer =request.user.customer
      order ,created = Order.objects.get_or_create(customer=customer ,complete=False)
      items =order.orderitem_set.all()
   else:
      items =[]
      order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
   return render(request, 'cart.html', {'items':items,'order':order})

def checkout(request):
   if request.user.is_authenticated:
      customer =request.user.customer
      order ,created = Order.objects.get_or_create(customer=customer ,complete=False)
      items =order.orderitem_set.all()
   else:
      items=[]
      order ={'get_cart_total':0,'get_cart_items':0,'shipping':False}
   return render(request, 'checkout.html', {'items':items,'order':order})

      
def register_view(request):
   if request.user.is_authenticated:
      return redirect('store')
   else:
      form =Creation_form()
      if request.method == 'POST': 
         form =Creation_form(request.POST)
         if form.is_valid():
            form.save()
            username =form.cleaned_data.get('username')
            password =form.cleaned_data.get('password1')
            acount =authenticate(username=username, password=password)
            login(request ,acount)
            return redirect('login')
      return render(request ,'register.html',{'form':form})

def logout_view(request):
   logout(request)
   return redirect('home')

def authin_view(request):
   if request.user.is_authenticated:
      return redirect('store')
   else:
      form =AuthenticationForm()
      if request.method == 'POST':
         username =request.POST.get('username')
         password =request.POST.get('password')
         user= authenticate(request ,username=username, password=password)
         if user is not None:
            request.session['pk'] =user.pk
            return redirect('verify')
      return render(request ,'auth.html',{'form':form})

def verify_view(request):
   if request.user.is_authenticated:
      return redirect('store')
   else:
      form = CodeForm(request.POST or None)
      pk =  request.session.get('pk')
      if pk:
         user =CustomUser.objects.get(pk=pk)
         code =user.code
         if not request.POST:
            url =f'https://messaging.ooredoo.qa/bms/soap/Messenger.asmx/HTTP_SendSms?customerID=2369&userName=QMarketer&userPassword=Y9g@A03U6rnzo&originator=Q-OTP&smsText={code}&recipientPhone={user.phone_number}&messageType=0&defDate=&blink=false&flash=false&Private=false'
            rq.get(url)
         if form.is_valid():
            num =form.cleaned_data.get('number')
            if str(code) == num:
               code.save()
               login(request, user) 
               return redirect('home')
            else:
               return redirect('login')
      return render(request, 'verify.html', {'form':form})

def update_item(request):
   data =json.loads(request.body)
   productId =data['productId']
   action =data['action']
   customer =request.user.customer
   product =Product.objects.get(id=productId)
   order ,created = Order.objects.get_or_create(customer=customer ,complete=False)
   orderitem ,created = OrderItem.objects.get_or_create(order=order ,product=product)

   if action == 'add':
      orderitem.quantity =(orderitem.quantity +1)
   elif action == 'remove':
      orderitem.quantity =(orderitem.quantity -1)
   orderitem.save()
   if orderitem.quantity <= 0 :
      orderitem.delete()
   return JsonResponse('item was add',safe=False)

@login_required()
@allowed_user(allowed_roles=['Customer'])
def repairs_view(request):
   form =Sim_form()
   if request.method == 'POST': 
      form =Sim_form(request.POST, request.FILES)
      if form.is_valid():
         form.save()
         return redirect('store')
   return render(request ,'repairs.html',{'form':form})


def prosessOrder(request):
   transaction_id =datetime.datetime.now().timestamp()
   data =json.loads(request.body)
   if request.user.is_authenticated:
      customer =request.user.customer
      order, created = Order.objects.get_or_create(
          customer=customer, complete=False)
      total =float(data['form']['total'])
      order.tansaction_id =transaction_id
      if total == order.get_cart_total:
        order.complete =True 
      order.save()
      if order.shipping == True:
         shippingAddress.objects.create(
             name=customer, order=order, location_url=data['shipping']['location_url'], area=data['shipping']['area'], street=data['shipping']['street'], building=data['shipping']['building'], address=data['shipping']['address'],city=data['shipping']['city'])
   else:
       print('user is not login')
   return JsonResponse('payment complete',safe=False)

@login_required()
def admin_panel(request):
   order =Order.objects.all()
   orderitem =OrderItem.objects.all()
   customer =Customer.objects.all()
   product =Product.objects.all()
      
   total_customer =customer.count()
   total_product =product.count()
   total_order =order.count()
   total_orderitem =orderitem.count()
   return render(request ,'index.html',{'orders':total_order,'customers':total_customer,'products':total_product,'orderitems':total_orderitem,'order':order})


def brands(request):
   brand =Brand.objects.all()
   return render(request, 'brand.html', {'brands':brand})


def order_detail(request):
   shipping =shippingAddress.objects.all()
   order =Order.objects.all()
   return render(request, 'order-detail.html', {'order': order, 'shipping': shipping})

def pos_system(request):
   product =Product.objects.all()
   catagory =Catagory.objects.all()
   order_item =OrderItem.objects.all()
   return render(request ,'pos.html',{'order':order_item,'catagory':catagory,'product':product})



