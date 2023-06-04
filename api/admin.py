from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from api.forms.add_user_form import CustomUserForm
from api.forms.company_forms import CompanyForm, AddCompanyForm
from django.contrib.auth import get_user_model
from api.models import Companies, Opinions, Categories

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


@admin.action(description="Accept selected Companies")
def accept_companies(modeladmin, request, queryset):
    queryset.update(status="accepted")

@admin.action(description="Reject selected Companies")
def reject_companies(modeladmin, request, queryset):
    queryset.update(status="rejected")

@admin.action(description="Ban selected Companies")
def ban_companies(modeladmin, request, queryset):
    queryset.update(status="banned")


class CompaniesAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ["name", "site", "status"]}),
        ("Auth", {"fields": ["username", "email", "token"]}),
        ("Pass", {"fields": ["password", "confirm_password"]})
    )

    add_fieldsets = (
        (None,
         {"fields": ("name", "site", "username", "email", "token", "password", "confirm_password", "status")}),
    )

    form = CompanyForm
    add_form = AddCompanyForm
    list_display = ('name', 'username', 'email', 'status')
    list_filter = [CompanyStatusListFilter]
    search_fields = ['name', 'username', 'email']
    actions = [accept_companies, reject_companies, ban_companies]

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        if obj is None:
            defaults["form"] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)


class OpinionsAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'company', 'rating_date')
    search_fields = ['company']

class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    search_fields = ['name']

admin.site.register(User, CustomUserAdmin)

admin.site.register(Companies, CompaniesAdmin)

admin.site.register(Opinions, OpinionsAdmin)

admin.site.register(Categories, CategoriesAdmin)
