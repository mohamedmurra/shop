from django.urls import path,re_path
from .views import  delete_brand, delete_catagory, store, login_view, logout_view, cart, checkout, update_brand, update_catagory, update_item, add_product, add_catagory, detail, register_view, account_view, whishlist, Product_main, main, Erro_view, search_bar, thankyou_view, admin_panel, contact_view, about_view,  admin_settigns, Subscriber_view,  update_product, delete_product, product,  add_brand, manage_coupon_view, delete_coupon, update_coupon, add_coupons,  shipping_address,product_report,order_report,Stock_Add,stock_transfere,order_list,admin_order_detail,user_list,user_detail,suplier_view,expenses_view,add_pur,Purchase_view,testo_view

urlpatterns = [
    path('',store,name='store'),
    path('products', main, name='main'),
    path('products/<slug>', Product_main, name='pro_main'),
    path('login/',login_view, name='login'),
    path('logout/',logout_view ,name='logout'),
    path('account/',account_view,name='account'),
    path('cart/',cart ,name='cart'),
    path('404/',Erro_view ,name='404'),
    path('thank_you/', thankyou_view, name='thank_you'),
    path('whishlist/', whishlist, name='whishlist'),
    path('checkout/',checkout ,name='checkout'),
    path('order-shipping/', shipping_address, name='order_shipping'),
    path('update_item',update_item ,name='update_item'),
    path('product/<slug>/', detail, name='detail'),
    path('register/',register_view,name='register'),
    path('search/',search_bar,name='search'),
    path('testo/',testo_view,name='testo'),
    path('subscribe/', Subscriber_view, name='Subscribe'),
    path('panel/', admin_panel, name='panel'),
    path('about/', about_view, name='about'),
    path('contact/', contact_view, name='contact'),
    path('panel/settings', admin_settigns, name='setting'),
    path('panel/stock/add', Stock_Add, name='add_stock'),
    path('panel/stock/transfer', stock_transfere, name='stock_transfer'),
    path('panel/product_csv/', product_report, name='product_csv'),
    path('panel/order_csv/', order_report, name='order_csv'),
    path('panel/coupons/add', add_coupons, name='add_coupons'),
    path('panel/coupons/update/<slug>', update_coupon, name='update_coupon'),
    path('panel/coupons/delete/<slug>', delete_coupon, name='delete_coupon'),
    path('panel/product/', product, name='product'),
    path('panel/add-product/', add_product, name='add-product'),
    path('panel/add-catagory/', add_catagory, name='add-catagory'),
    path('panel/update-catagory/<slug>', update_catagory, name='update-catagory'),
    path('panel/delete-catagory/<slug>', delete_catagory, name='delete-catagory'),
    path('panel/add-brand/', add_brand, name='add-brand'),
    path('panel/update-brand/<slug>', update_brand, name='update-brand'),
    path('panel/delete-brand/<slug>', delete_brand, name='delete-brand'),
    path('panel/update-product/<slug>', update_product, name='update_product'),
    path('panel/delete-product/<slug>', delete_product, name='delete_product'),
    path('panel/order/list', order_list, name='order-list'),
    path('panel/order/detail/<str:id>', admin_order_detail, name='update-order'),
    path('panel/pepoal/list', user_list, name='user-list'),
    path('panel/pepoal/edit/<str:id>', user_detail, name='user-detail'),
    path('panel/pepoal/supplier', suplier_view, name='supplier-list'),
    path('panel/expense/list', expenses_view, name='expense-list'),
    path('panel/purchase/list', Purchase_view, name='purr'),
    path('panel/purchase/add', add_pur, name='add-pur'),
]
