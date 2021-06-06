from django.urls import path
from .views import store, authin_view, verify_view, register_view, logout_view, cart, checkout, update_item, add_product, add_brand, add_catagory, register_view, prosessOrder, admin_panel, order_detail, brands,pos_system

urlpatterns = [
    path('',store,name='store'),
    path('store',store , name='home'),
    path('login/',authin_view, name='login'),
    path('verify/',verify_view, name='verify'),
    path('register/',register_view ,name='register'),
    path('logout/',logout_view ,name='logout'),
    path('cart/',cart ,name='cart'),
    path('checkout',checkout ,name='checkout'),
    path('update_item',update_item ,name='update_item'),
    path('add-product/',add_product, name='add-product'),
    path('add-catagory/',add_catagory,name='add-catagory'),
    path('add-brand/',add_brand ,name='add-brand'),
    path('repair/',register_view ,name='repair'),
    path('prosess-order/', prosessOrder, name='prosess_order'),
    path('panel/',admin_panel ,name='admin_panel'),
    path('order-detail/', order_detail, name='order_detail'),
    path('brands/', brands, name='brand_detail'),
    path('pos/',pos_system,name='pos'),
]
