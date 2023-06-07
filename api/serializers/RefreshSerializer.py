from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..utils.jwt_gen import generate_access_token, generate_refresh_token
from api.models import Companies
from django.conf import settings
import jwt

class RefreshSerializer(serializers.Serializer):


    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=150, read_only=True)
    name = serializers.CharField(default=None, read_only=True)
    role = serializers.CharField(max_length=255, read_only=True)
    access = serializers.CharField(max_length=255, read_only=True)
    refresh = serializers.CharField(max_length=255)

    def validate(self, data):
        refresh = data.get('refresh')

        if refresh is None:
            raise serializers.ValidationError(
                'Authentication credentials were not provided.')
        try:
            payload = jwt.decode(
                refresh, settings.SECRET_KEY, algorithms=['HS256']
            )
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError(
                'expired refresh token, please login again.')
        except jwt.DecodeError:
            raise serializers.ValidationError(
                {'detail': 'invalid token'})
        if payload['token_type'] != 'refresh':
            raise serializers.ValidationError(
                {'detail': 'invalid token'})
        if payload['user_type'] == 'company':
            user = Companies.objects.filter(id=payload.get('user_id')).first()
        else:
            users = get_user_model()
            user = users.objects.filter(id=payload.get('user_id')).first()
        if user is None:
            raise serializers.ValidationError("No active account found with the given credentials")
        access = generate_access_token(user,payload['user_type'])
        refresh = generate_refresh_token(user, payload['user_type'])
        if payload['user_type'] == 'company':
            name = user.name
        else:
            name = user.first_name +" "+ user.last_name
        return{
            'id': user.id,
            'name': name,
            'username': user.username,
            'role': payload['user_type'],
            'access': access,
            'refresh': refresh
        }

