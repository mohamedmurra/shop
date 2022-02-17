from django.contrib import admin
from .models import Acount
# Register your models here.

from django.contrib.auth.admin import UserAdmin



class AccountAdmin(UserAdmin):
 list_display = ('email', 'username', 'date_joined',
                 'last_login', 'is_admin', 'is_staff')
 search_fields = ('email', 'username',)
 read_only_fields = ('last_login', 'date_joined')
 filter_horizontal = ()
 list_filter = ()
 fieldsets = ()


admin.site.register(Acount, AccountAdmin)
