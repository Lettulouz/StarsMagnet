from rest_framework import serializers
from api.models import Companies
from django.contrib.auth.hashers import check_password
from django.db.models import Q
from ..utils.jwt_gen import generate_access_token, generate_refresh_token


class LoginCompanySerializer(serializers.Serializer):

    username = serializers.CharField(max_length=150, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=32, write_only=True)
    access = serializers.CharField(max_length=255, read_only=True)
    refresh = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        token = data.get("token", None)

        company = Companies.objects.filter((Q(username=username) | Q(email=username)), token=token).first()
        if not company:
            raise serializers.ValidationError({"detail": "No active account found with the given credentials"})
        if check_password(password, company.password):
            return {
                'access': generate_access_token(company, 'company'),
                'refresh': generate_refresh_token(company, 'company')
            }
        else:
            raise serializers.ValidationError({"detail": "No active account found with the given credentials"})

