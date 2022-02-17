from django.shortcuts import render ,redirect,get_object_or_404,HttpResponseRedirect,HttpResponse
from django.http import HttpRequest ,Http404
import random
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate ,login ,logout
from .models import Product, Catagory, Order, OrderItem, shippingAddress, Customer, Review, WhishList,MailMsg,Brand
from django.http import JsonResponse,HttpResponse
import json
from Coupon.models import Coupons
from Coupon.form import coupon_form
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from .forms import product_form, catagory_form, register_form, AuthenticationForm, CustomerUpdateForm, UserUpdateForm, ReviewForm, searsh_form, subscrbe_form, Contact_form, brand_form, coupon_update_form, order_update_form, Shipping_form
import datetime
from django.core.mail import send_mail,BadHeaderError
from .utils import CartCoocies,cartData
import string
import random
from django.db.models import Sum
from django.views.decorators.http import require_POST
import csv
# Create your views here.

def Subscriber_view(request):
   form = subscrbe_form(request.POST)
   if form.is_valid():
      form.save()
      messages.success(request, 'Subscribe successfully')
   else:
      messages.error(request,'Something went rong')
   return HttpResponseRedirect('/')

def detail(request,slug):
   qs = get_object_or_404(Product,slug=slug)
   comments = qs.comments.all().order_by('created')
   coounted = comments.count()
   related =Product.objects.filter(catagory=qs.catagory)
   comment_form = ReviewForm()
   new_comment =None
   if request.method == 'POST':
      comment_form = ReviewForm(request.POST)
      if comment_form.is_valid():
         new_comment =comment_form.save(commit=False)
         new_comment.product = qs
         new_comment.user = request.user.customer
         new_comment.save()
   data = cartData(request)
   cartItems = data['cartitems']
   items = data['items']
   order = data['order']
   wish = data['wish']
   Brands = data['Brands']

   return render(request, 'product.html', {'wish': wish, 'cartitems': cartItems, 'items': items, 'order': order, 'objects': qs, 'reviews': comments[:3], 'new_review': new_comment, 'form': comment_form, 'counted': coounted, 'products': related, 'Brands': Brands})

def manage_coupon_view(request):
   coupons =Coupons.objects.all()
   return render(request, 'home/coupons.html', {'coupons': coupons})

def account_view(request):
   if not request.user.is_authenticated:
    return redirect('login')
   orders = Order.objects.filter(customer=request.user.customer,complete=True)
   if request.method == 'POST':
     form = UserUpdateForm(request.POST or None,
                           request.FILES or None, instance=request.user)
     if form.is_valid():
        form.save()
        messages.success(request,'your acount been updated')
        return redirect('account')
   else:
      form=UserUpdateForm(
         initial={
            'email':request.user.email,
            'username':request.user.username,
            'first_name':request.user.first_name or '',
            'last_name':request.user.last_name or '',
            'phone_number':request.user.phone_number or '',
         }
      )
   data = cartData(request)
   cartItems = data['cartitems']
   items = data['items']
   order = data['order']
   wish = data['wish']
   Brands = data['Brands']

   return render(request, 'dashboard.html', {'cartitems': cartItems, 'items': items, 'order': order, 'wish': wish, 'form': form, 'orders': orders, 'Brands': Brands})

def Erro_view(request):
   data = cartData(request)
   cartItems = data['cartitems']
   items = data['items']
   order = data['order']
   wish = data['wish']
   return render(request, '404.html', {'cartitems': cartItems, 'items': items, 'order': order, 'wish': wish})

def add_product(request):
   form =product_form()
   if request.method == 'POST': 
      form =product_form(request.POST or None,request.FILES or None)
      if form.is_valid():
         form.save()
         return redirect('add-product')

   return render(request, 'home/add-prouduct.html', {'form': form})

@login_required()
def add_catagory(request):
   form =catagory_form()
   catagorys =Catagory.objects.all()
   if request.method == 'POST': 
      form =catagory_form(request.POST, request.FILES)
      if form.is_valid():
         form.save()
         return redirect('add-catagory')

   return render(request ,'home/add_catagory.html',{'form':form,'catagorys':catagorys})


def add_brand(request):
   form = brand_form()
   brands =Brand.objects.all()
   if request.method == 'POST':
      form = brand_form(request.POST, request.FILES)
      if form.is_valid():
         form.save()
         return redirect('add-brand')

   return render(request, 'home/add_brand.html', {'form': form,'brands':brands})


def add_coupons(request):
   form = coupon_update_form()
   if request.method == 'POST':
      form = coupon_update_form(request.POST)
      if form.is_valid():
         form.save()
         return redirect('coupons')

   return render(request, 'home/add_coupon.html', {'form': form})


def update_product(request,slug):
   product =get_object_or_404(Product,slug=slug)
   form = product_form(request.POST or None,
                         request.FILES or None, instance=product)
   if request.method == 'POST':
      if form.is_valid():
         form.save()
   return render(request, 'home/update_product.html', {'form': form, 'product': product})


def update_coupon(request, slug):
   coupon = get_object_or_404(Coupons, code=slug)
   form = coupon_update_form(request.POST or None,
                             request.FILES or None, instance=coupon)
   if request.method == 'POST':
      if form.is_valid():
         form.save()
   return render(request, 'home/update_coupon.html', {'form': form, 'coupon': coupon})


def delete_product(request,slug):
   product =get_object_or_404(Product,slug=slug)
   product.delete()
   return redirect('product')


def delete_coupon(request, slug):
   coupon = get_object_or_404(Coupons, code=slug)
   coupon.delete()
   return redirect('coupons')


def product(request):
   products =Product.objects.all()
   return render(request,'home/product.html',{'products':products})

def whishlist(request):
   page_obj = WhishList.objects.filter(customer=request.user.customer)
   data = cartData(request)
   cartItems = data['cartitems']
   items = data['items']
   order = data['order']
   wish = data['wish']
   Brands = data['Brands']
   return render(request, 'wishlist.html', {'wish': wish, 'cartitems': cartItems, 'items': items, 'order': order, 'page_obj': page_obj, 'Brands': Brands})

def store(request):
   shop_product = Product.objects.all()
   cata = Catagory.objects.all()
   top = Product.objects.all()[:5]
   product_filter = Product.objects.all()
   data =cartData(request)
   cartItems= data['cartitems']
   items = data['items']
   order = data['order']
   wish =data['wish']
   Brands = data['Brands']

   return render(request, 'shop.html', {'cartitems': cartItems, 'items': items, 'order': order, 'wish': wish, 'products': product_filter, 'catagory': cata, 'shop_product': shop_product, 'top': top, 'Brands': Brands})

def cart(request):
   form =coupon_form()
   data = cartData(request)
   Brands = data['Brands']
   if request.user.is_authenticated:
      wish = WhishList.objects.filter(customer=request.user.customer).count()
      try:
         customer = request.user.customer
         order ,created = Order.objects.get_or_create(customer=customer ,complete=False)
         items =order.orderitem_set.all()
         coupon = Coupons.objects.get(id=request.session['coupon_id'])
         order.coupon=coupon 
         order.save()
         cartItems = order.get_cart_items
      except :
         customer = request.user.customer
         order ,created = Order.objects.get_or_create(customer=customer ,complete=False)
         items =order.orderitem_set.all()
         cartItems = order.get_cart_items
      
   else:
      cookieData= CartCoocies(request)
      cartItems = cookieData['cartitems']
      order =cookieData['order']
      items =cookieData['items']
      wish =0
      
   return render(request, 'cart.html', {'items': items, 'order': order, 'form': form, 'wish': wish, 'cartitems': cartItems, 'Brands': Brands})

def checkout(request):
   if not request.user.is_authenticated:
    return redirect('login')
   data = cartData(request)
   Brands = data['Brands']
   wish = WhishList.objects.filter(customer=request.user.customer).count()
   customer = request.user.customer
   order ,created = Order.objects.get_or_create(customer=customer ,complete=False)
   items =order.orderitem_set.all()
   cartItems = order.get_cart_items
   return render(request, 'checkout.html', {'cartitems': cartItems, 'items': items, 'order': order, 'wish': wish , 'Brands': Brands})


def main(request):
   products =Product.objects.all()
   catagory =Catagory.objects.all()
   caount = products.count()
   p = Paginator(products, 6)
   page_number = request.GET.get('page', 1)
   try:
      page_obj = p.get_page(page_number)
   except PageNotAnInteger:
      page_obj = p.page(1)
   except EmptyPage:
      page_obj = p.page(p.page_number)
   data = cartData(request)
   cartItems = data['cartitems']
   items = data['items']
   order = data['order']
   wish = data['wish']
   Brands = data['Brands']

   return render(request, 'main.html', {'wish': wish, 'cartitems': cartItems, 'items': items, 'order': order, 'products': products, 'catagorys': catagory, 'count': caount, 'page_obj': page_obj, 'Brands': Brands})

def Product_main(request ,slug):
   catagory =Catagory.objects.all()
   catagory_filter=Catagory.objects.filter(slug=slug)
   product =Product.objects.filter(catagory__slug=slug)
   cata_name = Catagory.objects.get(slug=slug)
   caount =product.count()
   p = Paginator(product, 6)
   page_number =request.GET.get('page',1)
   try:
      page_obj = p.get_page(page_number)
   except PageNotAnInteger:
      page_obj = p.page(1)
   except EmptyPage:
      page_obj = p.page(p.page_number)
   data = cartData(request)
   cartItems = data['cartitems']
   items = data['items']
   order = data['order']
   wish = data['wish']
   Brands = data['Brands']

   return render(request, 'pro_main.html', {'wish': wish, 'cartitems': cartItems, 'items': items, 'order': order, 'products': product, 'catagorys': catagory, 'count': caount, 'page_obj': page_obj, 'cata_name':cata_name , 'Brands': Brands})

def logout_view(request):
   logout(request)
   return redirect('store')

def login_view(request):
   if request.user.is_authenticated:
      return redirect('store')
   else:
      if request.POST:
         form = AuthenticationForm(request.POST)
         if form.is_valid():
            email =form.cleaned_data.get('email')
            password =form.cleaned_data.get('password')
            user =authenticate(email=email ,password=password)
            if user:
               login(request, user)
               if request.user.is_superuser:
                  return redirect('panel')
               return redirect('store')
      else:
         form =AuthenticationForm()
      return render(request,'login.html',{'form':form})

def update_item(request):
   data =json.loads(request.body)
   customer = request.user.customer
   productId = data['productId']
   action =data['action']
   product = Product.objects.get(id=productId)
   if action == 'wish':
      wishlist, created = WhishList.objects.get_or_create(
           customer=customer, product=product)
   else:
      order, created = Order.objects.get_or_create(
         customer=customer, complete=False)
      orderitem ,created =OrderItem.objects.get_or_create(order=order,product=product)

      if action == 'add':
         orderitem.quantity =(orderitem.quantity +1)
      elif action == 'remove':
         orderitem.quantity = (orderitem.quantity -1)
      orderitem.save()
      if orderitem.quantity <= 0:
         orderitem.delete()
   return JsonResponse('item was add', safe=False)

def about_view(request):
   data = cartData(request)
   cartItems = data['cartitems']
   items = data['items']
   order = data['order']
   wish = data['wish']
   Brands = data['Brands']
   return render(request, 'about.html', {'cartitems': cartItems, 'items': items, 'order': order, 'wish': wish, 'Brands': Brands})

def thankyou_view(request):
   data = cartData(request)
   cartItems = data['cartitems']
   items = data['items']
   order = data['order']
   wish = data['wish']
   Brands = data['Brands']
   orders =Order.objects.filter(customer=request.user.customer,complete=True).latest('date_orderd')
   return render(request, 'thankyou.html', {'orders': orders, 'cartitems': cartItems, 'items': items, 'order': order, 'wish': wish, 'Brands': Brands})

def checkout_prosses(request):
   data =json.loads(request.body)
   customer = request.user.customer
   order= Order.objects.get(
       customer=customer, complete=False)
   total =data['totall']
   order.complete =True
   order.status ='Paid'
   try :
       del request.session['coupon_id']
   except :
      None
   order.save()
   if order.get_cart_total_after_discount > 0:
      shippingAddress.objects.create(
         name=customer,
         order=order,
         phone_number=data['shipping_for']['phone_number'],
         address=data['shipping_for']['address'],
         city=data['shipping_for']['city'],
         state=data['shipping_for']['state'],
         aria=data['shipping_for']['aria'],
      )
   return render(request,'payment.html',safe=False)

def search_bar(request):
   search_items = request.GET['items']
   products =Product.objects.filter(name__icontains=search_items)
   data = cartData(request)
   cartItems = data['cartitems']
   items = data['items']
   order = data['order']
   wish = data['wish']
   Brands = data['Brands']
   return render(request, 'search_result.html', {'Products': products, 'count': products.count(), 'cartitems': cartItems, 'items': items, 'order': order, 'wish': wish,'Brands': Brands})

def searsh_order(request):
   searsh_order =request.GET['order']
   orders = Order.objects.filter(tansaction_id__icontains=searsh_order)
   return render(request, 'home/searsh_order.html', {'orders': orders,'count':orders.count(),})

def searsh_product(request):
   searsh_product = request.GET['product']
   products = Product.objects.filter(name__icontains=searsh_product)
   return render(request, 'home/searsh_product.html', {'products': products, 'count': products.count(), })

def admin_panel(request):
   orders = Order.objects.filter(complete=True).order_by('date_orderd',)
   sales=0
   for order in orders:
      sales += order.get_cart_total_after_discount
   products =Product.objects.all()
   users =Customer.objects.all()
   return render(request, 'home/dashboard.html', {'products_count': products.count(), 'orders_count': orders.count(), 'users_count': users.count(), 'sales': sales, 'orders': orders})

def transaction_view(request):
   orders = Order.objects.filter(complete=True).order_by('date_orderd',)
   count =orders.count()
   p = Paginator(orders, 10)
   page_number = request.GET.get('page', 1)
   try:
      page_obj = p.get_page(page_number)
   except PageNotAnInteger:
      page_obj = p.page(1)
   except EmptyPage:
      page_obj = p.page(p.page_number)
   return render(request, 'home/transactions.html', {'orders': page_obj,'count':count})

def update_transaction(request,slug):
   order = get_object_or_404(Order,tansaction_id=slug)
   form = order_update_form(request.POST or None,instance=order)
   if form.is_valid():
      form.save()
   return render(request, 'home/update_order.html', {'form': form, 'order': order})

def shipping_address(request):
   if request.user.is_authenticated:
      customer =request.user.customer
      form = Shipping_form()
      if request.method =='POST':
         form = Shipping_form(request.POST)
         if form.is_valid():
            instane =form.save(commit =False)
            instane.name =customer
            instane.order = Order.objects.get(
               customer=customer, complete=False)
            instane.save()
            return redirect('checkout')
   else:
      form = Shipping_form()
   data = cartData(request)
   cartItems = data['cartitems']
   items = data['items']
   order = data['order']
   wish = data['wish']
   Brands = data['Brands']
   return render(request,'shipping.html',{'form':form, 'cartitems': cartItems, 'items': items, 'order': order, 'wish': wish, 'Brands': Brands})
         

def admin_settigns(request):
   form =UserUpdateForm(
       initial={
           'email': request.user.email,
           'username': request.user.username,
           'first_name': request.user.first_name or '',
           'last_name': request.user.last_name or '',
           'phone_number': request.user.phone_number or '',
       }
   )
   if request.method == 'POST':
      form =UserUpdateForm(
          request.POST or None,
          request.FILES or None, instance=request.user
      )
      if form.is_valid():
         form.save()
         return redirect('setting')
   return render(request, 'home/settings.html', {'form': form})

def delete_Brand(request,slug):
   brand =get_object_or_404(Brand,slug=slug)
   brand.delete()
   return redirect('panel')

def register_view(request):
   if request.user.is_authenticated:
      return redirect('store')
   else:
      if request.POST:
         form = register_form(request.POST)
         if form.is_valid():
            form.save()
            return redirect('login')
      else:
         form =register_form()
   return render(request, 'signup.html', {'form': form})

def contact_view(request):
   form =Contact_form()
   if request.method == 'POST':
      form =Contact_form(request.POST)
      if form.is_valid():
         subject = form.cleaned_data['subject']
         from_mail=form.cleaned_data['email']
         message =form.cleaned_data['message']
         try:
            send_mail(subject, message, from_mail, ['suport@gmail.com'])
         except BadHeaderError:
            return HttpResponse('Invalid request')
         return redirect('store')
   data = cartData(request)
   cartItems = data['cartitems']
   items = data['items']
   order = data['order']
   wish = data['wish']
   Brands = data['Brands']
   return render(request, 'contact.html', {'form':form,'cartitems': cartItems, 'items': items, 'order': order, 'wish': wish, 'Brands': Brands})

def shipping_view(request):

   not_shipped = shippingAddress.objects.all()
   count = not_shipped.count()
   p = Paginator(not_shipped, 10)
   page_number = request.GET.get('page', 1)
   try:
      page_obj = p.get_page(page_number)
   except PageNotAnInteger:
      page_obj = p.page(1)
   except EmptyPage:
      page_obj = p.page(p.page_number)
   
   return render(request,'home/shipping.html',{'not_shipped':page_obj,'count':count})

def Payment_prosses(request):
   order_id =request.session.get('order_id')
   order =get_object_or_404(Order,id=order_id)
   host =request.get_host()

   paypal_dict ={
      'business':settings.PAYPAL_RECEIVER_EMAIL,
      'amount': '%.2f' % order.get_get_cart_total_after_discount().quantity(
         Decimal('.01')),
      'item_name':'Order{}'.format(order.id),
      'invoice':str(order.id),
      'currency_code':'USD',
      'notify_url':'http://{}{}'.format(host,reverse('paypal_ipn')),
      'return_url':'http://{}{}'.format(host,reverse('payment_done')),
      'cancel_return':'http: // {}{}'.format(host,reverse('payment_cancelled')),
   }
   form =PayPalPaymentsForm(initial=paypal_dict)
   return render(request,'prosses_payment.html',{'order':order,'form':form})

def product_report(request):
   products =Product.objects.all()
   response =HttpResponse(content_type='text/csv')
   response['Content-Disposition']='attachment; filename=products.csv'
   writer =csv.writer(response)
   writer.writerow(['Product name','catagory','discount','price','brand','stack','description'])

   for product in products:
      writer.writerow([product.name, product.catagory, product.discount,
                      product.price, product.brand, product.stack, product.description])
   return response


def order_report(request):
   orders =Order.objects.filter(complete=True)
   response =HttpResponse(content_type='text/csv')
   response['Content-Disposition']='attachment; filename=order.csv'
   writer =csv.writer(response)
   writer.writerow(['tansaction_id','customer','catagory','product_name','price','quantity','discount','total','date'])

   for order in orders:
      for item in order.orderitem_set.all():
         writer.writerow(
             [order.tansaction_id, order.customer, item.product.catagory, item.product.name, item.product.price, item.quantity, item.product.discount, order.get_cart_total_after_discount, order.date_orderd])

   return response