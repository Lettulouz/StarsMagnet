from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from rest_framework.authentication import BaseAuthentication
from api.models import Companies
from django.conf import settings
from rest_framework import exceptions
from django.db.models import Q
import jwt

USER = get_user_model()


class UsernameOrEmailBackend(ModelBackend):
    """
    Authentication based on email or login, used in admin panel.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Method that check credential of user.
        :param request: request
        :param username: username or email
        :param password: password
        :param kwargs: additional key arguments.
        :return: user if exits, otherwise raise error.
        """
        if username is None:
            username = kwargs.get(USER.USERNAME_FIELD)

        case_insensitive_username_field = '{}__iexact'.format(USER.USERNAME_FIELD)
        users = USER._default_manager.filter(
            Q(**{case_insensitive_username_field: username}) | Q(email__iexact=username))

        for user in users:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        if not users:
            USER().set_password(password)


class JWTAuth(BaseAuthentication):
    """
    Authentication based on JWT.
    """
    def authenticate(self, request):
        """
        Authenticate users and companies by jwt.
        Raise error if token is invalid or user isn't provided to log in.
        :param request: request
        :return: users or companies object if authenticated, otherwise raise error.
        """
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None
        try:
            access = auth_header.split(' ')[1]
            payload = jwt.decode(
                access, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed(
                'access token expired')
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed(
                {'detail': 'invalid token'})
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')
        if payload['token_type'] != 'access':
            raise exceptions.AuthenticationFailed(
                {'detail': 'invalid token'})
        if payload['user_type'] == 'company':
            user = Companies.objects.filter(id=payload.get('user_id'), status='accepted').first()
        else:
            users = get_user_model()
            user = users.objects.filter(id=payload.get('user_id'), is_active=True).first()
        if user is None:
            raise exceptions.AuthenticationFailed({"detail": "No active account found with the given credentials"})

        return (user, None)
