# jwt
import jwt
# django
from .models import User
from django.conf import settings
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from .utils import get_tokens_for_user, Util, generate_token
from .serializers import Login, RegisterSerializer, ResendChangedEmailSerializer, \
    UserSerializer, EmailVerificationSerializer
# rest_framework
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import CreateModelMixin
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.viewsets import ModelViewSet, GenericViewSet


def sending_email_verfication(request, user_data):
    user = User.objects.get(email=user_data['email'])
    token = RefreshToken.for_user(user).access_token
    current_site = get_current_site(request).domain
    relativeLink = reverse('email-verify')
    absurl = 'http://' + current_site + relativeLink + "?token=" + str(token)
    email_body = '' + absurl
    data = {'email_body': email_body,
            'email_subject': '', 'email_to': user.email}
    Util.send_email(data)


class RegisterViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.data['email'])
        sending_email_verfication(request, serializer.data)
        return Response({"message": "user create successfully."}, status=status.HTTP_200_OK)


class LoginView(CreateModelMixin, GenericViewSet):
    serializer_class = Login

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        try:
            user = User.objects.get(email=serializer.validated_data['email'])
            if user.check_password(serializer.validated_data['password']):
                if not user.is_verify:
                    token = {
                        "token": generate_token(user.id),
                        "message": "please verify your account."
                    }
                    return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data=token)

                token = get_tokens_for_user(user)
                return Response(token, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_403_FORBIDDEN)


class VerifyEmail(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verify:
                user.is_verify = True
                user.save()

            return Response({"email": "Verified Successfully."}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            return Response({"error": "Activation expired try again."}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({"error": "Invalid Token"}, status=status.HTTP_400_BAD_REQUEST)


class ResendChangeEmailView(CreateModelMixin, GenericViewSet):
    serializer_class = ResendChangedEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            token = serializer.validated_data['token']
            email = serializer.validated_data['email']
            payload = jwt.decode(
                token, key='time is the only asset', algorithms='HS256')

            user = User.objects.get(id=payload['sub'])
            user_data = {"email": user.email}

            if User.objects.filter(email=email).exists():
                sending_email_verfication(request, user_data)
                return Response({"message": "Email Resended!"}, status=status.HTTP_200_OK)

            user.email = email
            user.save()
            user_data = {"email": user.email}
            sending_email_verfication(request, user_data)
        return Response({"message": "Email Resended!"}, status=status.HTTP_200_OK)


class UserView(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
