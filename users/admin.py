from django.contrib import admin
from .models import CustomUser
from codes.forms import Creation_form
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class CustomUserAdmin(UserAdmin):
 models =CustomUser
 add_form = Creation_form


admin.site.register(CustomUser, CustomUserAdmin)
