from .views import Product_serli, shipping_api, Order_create_api, create_orderitems_api, repairs_api, Customer_api, RegistrationView
from django.urls import path



urlpatterns = [
    path('product', Product_serli.as_view()),
    path('shipping',shipping_api.as_view()),
    path('create-order', Order_create_api.as_view()),
    path('create-orderitems',create_orderitems_api.as_view()),
    path('repairs', repairs_api.as_view()),
    path('customer', Customer_api.as_view()),
    path('register', RegistrationView),
]
