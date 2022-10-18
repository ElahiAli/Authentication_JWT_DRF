from asyncio import exceptions
from dataclasses import dataclass
from django.conf import settings
from django.core.mail import EmailMessage
import jwt
import datetime
import time

# def generate_token(user_id):
#     now = int(time.time())
#     exp_time = int(now) + (2628000*60)
#     payload_data = {
#         'sub' : user_id
#     }
#     mysecret = "who know's?1245"
#     token = jwt.encode(
#         payload = payload_data,
#         key = mysecret
#     )
#     return token


def access_token(id, username, email):
    return jwt.encode({
        'user_id': id,
        'username': username,
        'email': email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),

    }, settings.SECRET_KEY, algorithm='HS256')

# def decode_access_token(token):
#     try:
#         payload = jwt.decode(token, 'access_token', algorithms='HS256')
#         return payload['user_id']
#     except:
#         raise exceptions.AuthenticationFailed('unathenticated!')


def refresh_token(id, username, email):
    return jwt.encode({
        'user_id': id,
        'username': username,
        'email': email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
    }, 'refresh_secret', algorithm='HS256')
