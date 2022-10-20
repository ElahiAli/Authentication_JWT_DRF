from core.models import User
from .utils import get_tokens_for_user, Util
from .serializers import RegisterSerializer, UserSerializer, EmailVerificationSerializer
from rest_framework import generics, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings


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


class RegisterViewSet(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.data['email'])
        sending_email_verfication(request, serializer.data)
        return Response({"message": "user create successfully."}, status=status.HTTP_200_OK)


@api_view(['POST'])
def Login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = User.objects.get(email=email)
        if user.check_password(password):
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


class UserView(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
