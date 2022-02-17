from django.contrib import admin
from . models import Product, shippingAddress, OrderItem, Order, Customer, Catagory,Review,WhishList,Brand,Tags,Subscriber,MailMsg
# Register your models here.

admin.site.register(Product)
admin.site.register(Review)
admin.site.register(shippingAddress)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Customer)
admin.site.register(Catagory)
admin.site.register(WhishList)
admin.site.register(Brand)
admin.site.register(Tags)
admin.site.register(MailMsg)
admin.site.register(Subscriber)
