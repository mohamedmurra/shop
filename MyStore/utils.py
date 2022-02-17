from .models import *
import json
def CartCoocies(request):
       try:
         cart = json.loads(request.COOKIES['cart'])
       except:
         cart={}
       wish=0
       items =[]
       order = {'get_cart_total': 0, 'get_cart_items': 0}
       cartItems =order['get_cart_items']
       for i in cart:
         try:
            cartItems += cart[i]['quantity']
            product =Product.objects.get(id=i)
            total =(product.price * cart[i]['quantity'])
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']
            item ={
               'product':{
                  'id':product.id,
                  'name':product.name,
                  'price':product.price,
                  'image':product.image
               },
               'quantity':cart[i]['quantity'],
               'get_total':total,
            }
            items.append(item)
         except :
            pass
       return {'items': items, 'order': order, 'cartitems': cartItems}

def cartData(request):
    Brands =Brand.objects.all()
    if request.user.is_authenticated:
      customer = request.user.customer
      wish = WhishList.objects.filter(customer=customer).count()
      order, created = Order.objects.get_or_create(
          customer=customer, complete=False)
      items = order.orderitem_set.all()
      cartItems = order.get_cart_items
    else:
      cookieData = CartCoocies(request)
      cartItems = cookieData['cartitems']
      order = cookieData['order']
      items = cookieData['items']
      wish = 0
    return {'items': items, 'order': order, 'cartitems': cartItems,'wish':wish,'Brands':Brands}
