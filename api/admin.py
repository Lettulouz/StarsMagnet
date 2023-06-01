from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from api.forms.add_user_form import CustomUserForm
from api.forms.add_company_form import CompanyForm
from django.contrib.auth import get_user_model
from api.models import Companies, Opinions

# Register your models here.

User = get_user_model()

# TODO: adding forms/ update form for company

class CompanyStatusListFilter(admin.SimpleListFilter):
    title = "company status"
    parameter_name = "status"

    def lookups(self, request, model_admin):
        return[
            ('pending', 'Waiting for acceptation'),
            ('accepted', 'Application accepted'),
            ('rejected', 'Application rejected'),
            ('banned', 'Company banned')
        ]

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        return queryset.filter(status=self.value())


# Registered models

class CustomUserAdmin(UserAdmin):
    form = CustomUserForm
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active')


class CompaniesAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ["name", "site", "status"]}),
        ("Auth", {"fields": ["login", "email", "token"]}),
        ("Pass", {"fields": ["password", "confirm_password"]})
    )

    add_fieldsets = (
        (None,
         {"fields": ("name", "site", "login", "email", "token", "password", "confirm_password", "status")}),
    )

    form = CompanyForm
    list_display = ('name', 'login', 'email', 'status')
    list_filter = [CompanyStatusListFilter]
    search_fields = ['name', 'login', 'email']

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)


class OpinionsAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'company', 'rating_date')
    search_fields = ['company']


admin.site.register(User, CustomUserAdmin)

admin.site.register(Companies, CompaniesAdmin)

admin.site.register(Opinions, OpinionsAdmin)
