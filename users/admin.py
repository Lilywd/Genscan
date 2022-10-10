from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
   list_display = ('email', 'username')
   search_fields = ('email', 'username')
   
   fieldsets = ()
   filter_horizontal = ()
   list_filter = ()
 
 
admin.site.register(User, CustomUserAdmin)
