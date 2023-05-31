from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from api.forms.add_user_form import CustomUserForm
from django.contrib.auth import get_user_model
from django.contrib.admin.filters import AllValuesFieldListFilter
from api.models import Companies, Opinions

# Register your models here.

User = get_user_model()

# TODO: adding forms

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserForm
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active')


class CompaniesAdmin(admin.ModelAdmin):
    list_display = ('name', 'login', 'email', 'status')
    # TODO: filter by status
    # list_filter = (('status',AllValuesFieldListFilter))


class OpinionsAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'company', 'rating_date')


admin.site.register(User, CustomUserAdmin)

admin.site.register(Companies, CompaniesAdmin)

admin.site.register(Opinions, OpinionsAdmin)
