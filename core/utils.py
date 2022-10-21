from asyncio import exceptions
from dataclasses import dataclass
from django.conf import settings
from django.core.mail import EmailMessage
import jwt
import datetime
import time
from django.core.mail import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['email_to']])
        email.send()


def generate_token(user_id):
    now = int(time.time())
    exp_time = int(now) + (2628000*60)
    payload_data = {
        'sub': user_id
    }
    mysecret = "time is the only asset"
    token = jwt.encode(
        payload=payload_data,
        key=mysecret
    )
    return token


# def access_token(id,):
#     return jwt.encode({
#         'user_id': id,
#         'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
#         'iat': datetime.datetime.utcnow()
#     }, settings.SECRET_KEY, algorithm='HS256')


# def access_token(user):
#     jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
#     jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

#     payload = jwt_payload_handler(user)
#     token = jwt_encode_handler(payload)
#     return token


# def refresh_token(id, username, email):
#     return jwt.encode({
#         'user_id': id,
#         'username': username,
#         'email': email,
#         'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
#         'iat': datetime.datetime.utcnow()
#     }, 'refresh_secret', algorithm='HS256')


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
