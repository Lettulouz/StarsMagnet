from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import ValidationError, FieldError
from django.db.models import Avg
from django.forms.models import BaseInlineFormSet
from api.forms.add_user_form import CustomUserForm, CustomUserChanger
from api.forms.company_forms import CompanyForm, AddCompanyForm
from django.contrib.auth import get_user_model
from api.models import Companies, Opinions, Categories, CategoriesOfCompanies

# Register your models here.

User = get_user_model()


class CompanyStatusListFilter(admin.SimpleListFilter):
    """
    Method for filter companies by status.
    Inherited from SimpleListFilter.
    """
    title = "company status"
    parameter_name = "status"

    def lookups(self, request, model_admin):
        """
        :param request: request
        :param model_admin: admin model
        :return: list of possible statuses.
        """
        return[
            ('pending', 'Waiting for acceptation'),
            ('accepted', 'Application accepted'),
            ('rejected', 'Application rejected'),
            ('banned', 'Company banned')
        ]

    def queryset(self, request, queryset):
        """
        Method for filter Companies by status.
        :param request: request
        :param queryset: companies queryset
        :return: filtered queryset
        """
        if self.value() is None:
            return queryset
        return queryset.filter(status=self.value())


# Registered models

class CustomUserAdmin(UserAdmin):
    """
    Custom users management in admin panel.
    Contains custom forms, list, and filters.
    Inherited from UserAdmin
    """
    form = CustomUserChanger
    add_form = CustomUserForm
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active')

class CompaniesInlineFormSet(BaseInlineFormSet):
    """
    Form for relations between categories and companies.
    Check if relation already exists.
    """

    def add_fields(self, form, index):
        super().add_fields(form, index)
        form.fields['company'].required = False
        form.fields['category'].required = False

    def clean(self):
        super().clean()
        existing_relations = set()
        for form in self.forms:

            if not form.cleaned_data.get('company') or not form.cleaned_data.get('category'):
                form.add_error('company', 'This field is required')
                form.add_error('category', 'This field is required')
                continue
            if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                company = form.cleaned_data['company']
                category = form.cleaned_data['category']
                relation = (company, category)
                if relation in existing_relations:
                    form.add_error('company', 'Duplicated relation')
                    form.add_error('category', 'Duplicated relation')
                existing_relations.add(relation)

class JunctionTableInline(admin.TabularInline):
    """
    Class for management relations between categories and companies.
    """
    model = CategoriesOfCompanies
    extra = 0
    formset = CompaniesInlineFormSet



@admin.action(description="Accept selected Companies")
def accept_companies(modeladmin, request, queryset):
    """
    Action for accept multiple companies.
    :param modeladmin: admin model.
    :param request: request.
    :param queryset: Companies queryset.
    """
    queryset.update(status="accepted")

@admin.action(description="Reject selected Companies")
def reject_companies(modeladmin, request, queryset):
    """
    Action for reject multiple companies.
    :param modeladmin: admin model.
    :param request: request.
    :param queryset: Companies queryset.
    """
    queryset.update(status="rejected")

@admin.action(description="Ban selected Companies")
def ban_companies(modeladmin, request, queryset):
    """
    Action for ban multiple companies.
    :param modeladmin: admin model.
    :param request: request.
    :param queryset: Companies queryset.
    """
    queryset.update(status="banned")


class CompaniesAdmin(admin.ModelAdmin):
    """
    Custom companies management in admin panel.
    Contains custom fieldsets, forms, list, filters and actions.
    Provides adding relation between company and category.
    """

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
    list_display = ('name', 'username', 'email', 'status', 'rating')
    list_filter = [CompanyStatusListFilter]
    search_fields = ['name', 'username', 'email']
    actions = [accept_companies, reject_companies, ban_companies]
    inlines = [JunctionTableInline]

    def rating(self, obj):
        """
        Method that return average rating for companies list.
        :param obj: Companies object.
        :return: average rating.
        """
        average = Opinions.objects.filter(company=obj).aggregate(average=Avg('rating'))['average']
        return average
    rating.admin_order_field = 'opinions__rating'
    def get_queryset(self, request):
        """
        Method that return queryset of companies, used to sort companies by average rating.
        :param request: request
        :return: Companies queryset.
        """
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(srednia=Avg('opinions__rating'))
        return queryset
    def get_fieldsets(self, request, obj=None):
        """
        Method that return add_fieldsets at adding company or
        standard fieldset at editing company.
        :param request: request
        :param obj: company object.
        :return: fieldsets
        """
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """
        Method that return add_form at adding company or
        standard form at editing company.
        :param request: request
        :param obj: company object.
        :return: form
        """
        defaults = {}
        if obj is None:
            defaults["form"] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)


class OpinionsAdmin(admin.ModelAdmin):
    """
    Management for opinions in admin, contains custom list display
    and search bar.
    """
    list_display = ('user', 'rating', 'company', 'rating_date')
    search_fields = ['company__name', 'user__username']

class CategoriesAdmin(admin.ModelAdmin):
    """
    Management for categories in admin, contains custom list display, search bar
    and provides adding relation between category and company.
    """
    list_display = ('name', 'icon')
    search_fields = ['name']
    inlines = [JunctionTableInline]

admin.site.register(User, CustomUserAdmin)

admin.site.register(Companies, CompaniesAdmin)

admin.site.register(Opinions, OpinionsAdmin)

admin.site.register(Categories, CategoriesAdmin)
