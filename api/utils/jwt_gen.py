import datetime
import jwt
from django.conf import settings


def generate_access_token(user, user_type="user"):
    """
    Method to generate access jwt for users and companies
    :param user: user or company object
    :param user_type: type of user, default "user"
    :return: access token
    """
    access_token_payload = {
        'token_type': 'access',
        'user_id': user.id,
        'user_type': user_type,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=5),
        'iat': datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(access_token_payload,
                              settings.SECRET_KEY, algorithm='HS256')
    return access_token


def generate_refresh_token(user, user_type="user"):
    """
    Method to generate refresh jwt for users and companies
    :param user: user or company object
    :param user_type: type of user, default "user"
    :return: refresh token
    """
    refresh_token_payload = {
        'token_type': 'refresh',
        'user_id': user.id,
        'user_type': user_type,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
    }
    refresh_token = jwt.encode(
        refresh_token_payload, settings.SECRET_KEY, algorithm='HS256')

    return refresh_token