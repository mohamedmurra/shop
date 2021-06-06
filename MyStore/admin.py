from django.contrib import admin
from . models import Product, shippingAddress, repairs, OrderItem, Order, Customer, Brand, Catagory
# Register your models here.

admin.site.register(Product)
admin.site.register(shippingAddress)
admin.site.register(repairs)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Customer)
admin.site.register(Brand)
admin.site.register(Catagory)
