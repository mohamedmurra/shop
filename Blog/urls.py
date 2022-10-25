from django.urls import path
from .views import homepage, create_blog_view, update_blog_view, delete_blog_view, post_detail,cata_fil,blog_manage,delete_catagory,update_catagory,create_catagory


urlpatterns = [
    path('', homepage,name='blog_home'),
    path('create_post/', create_blog_view,name='create_post'),
    path('update_blog_view/<slug>', update_blog_view ,name='update_post'),
    path('delete_blog_view/<slug>', delete_blog_view,name='delete_post'),
    path('post_detail/<slug>', post_detail,name='post_detail'),
    path('update_catagory/<slug>', update_catagory ,name='update_blog_catgory'),
    path('delete_catagory/<slug>', delete_catagory,name='delete_blog_catagory'),
    path('add_blog_Catagory/', create_catagory,name='add_blog_Catagory'),
    path('post_filter/<slug>', cata_fil,name='post_filter'),
    path('blog_manage',blog_manage,name='blog_manage'),
]
