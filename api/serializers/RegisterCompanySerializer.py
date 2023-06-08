from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from api.models import Companies, CategoriesOfCompanies, Categories
from django.contrib.auth.hashers import make_password
from ..utils.generate_token import generate_token


User = get_user_model()


def unique_username(value):
    if User.objects.filter(username=value).exists() or Companies.objects.filter(username=value).exists():
        raise serializers.ValidationError("This field must be unique.")


def unique_email(value):
    if User.objects.filter(email=value).exists() or Companies.objects.filter(email=value).exists():
        raise serializers.ValidationError('This field must be unique.')


def category_exists(category_id):
    return Categories.objects.filter(id=category_id).exists()


class RegisterCompanySerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)
    categories = serializers.ListField(child=serializers.IntegerField(), required=True)

    email = serializers.EmailField(
        required=True,
        validators=[unique_email]
    )

    username = serializers.CharField(
        required=True,
        validators=[unique_username]
    )

    class Meta:
        model = Companies
        fields = ('name', 'site', 'username', 'password', "confirm_password", "email", "categories")

    def validate(self, attr):
        if attr['password'] != attr['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords must be the same"})
        return attr

    def save(self):

        company = Companies.objects.create(
            name=self.validated_data['name'],
            site=self.validated_data['site'],
            username=self.validated_data['username'],
            password=make_password(self.validated_data['password']),
            token=generate_token(),
            email=self.validated_data['email']
        )

        company.save()
        categories = self.validated_data.get('categories')

        for category in categories:
            if category_exists(category):
                new_category = CategoriesOfCompanies.objects.create(
                    company_id=company.id,
                    category_id=category
                )
                new_category.save()

        return company
