from django.contrib import admin
from .models import comment, blog, Catagory
# Register your models here.


admin.site.register(comment)
admin.site.register(blog)
admin.site.register(Catagory)
