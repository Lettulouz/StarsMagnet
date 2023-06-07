from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db.models import Q
from ..utils.jwt_gen import generate_access_token, generate_refresh_token
User = get_user_model()

class LoginSerializer(serializers.Serializer):

    password = serializers.CharField(max_length=128, write_only=True)
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=150)
    name = serializers.CharField(default=None, read_only=True)
    access = serializers.CharField(max_length=255, read_only=True)
    refresh = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):

        username = data.get("username", None)
        password = data.get("password", None)

        case_insensitive_username_field = '{}__iexact'.format(User.USERNAME_FIELD)
        user = User._default_manager.filter(
            (Q(**{case_insensitive_username_field: username}) | Q(email__iexact=username)), is_active=True).first()
        if not user:
            raise serializers.ValidationError({"detail": "No active account found with the given credentials"})
        if user.check_password(password) and user.is_active:
            return {
                'id': user.id,
                'name': user.first_name +" "+ user.last_name,
                'username': user.username,
                'access': generate_access_token(user),
                'refresh': generate_refresh_token(user)
            }
        else:
            raise serializers.ValidationError({"detail": "No active account found with the given credentials"})
        return data