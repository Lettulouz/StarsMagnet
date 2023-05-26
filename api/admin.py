from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from api.forms.add_user_form import CustomUserForm
from django.contrib.auth import get_user_model
# Register your models here.

User = get_user_model()


class CustomUserAdmin(UserAdmin):
     add_form = CustomUserForm
     list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser')
     list_filter = ('is_staff', 'is_superuser', 'is_active')


admin.site.register(User, CustomUserAdmin)
