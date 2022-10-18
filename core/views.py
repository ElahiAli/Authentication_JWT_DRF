from django.shortcuts import render

from core.models import User
from core.utils import access_token, refresh_token
from .serializers import RegisterSerializer, UserSerializer
from rest_framework import generics, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import api_view


class RegisterViewSet(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "user create successfully."}, status=status.HTTP_200_OK)


@api_view(['POST'])
def Login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = User.objects.get(email=email)
        if user.check_password(password):
            token = {
                "access-token": access_token(user.id, user.username, user.email),
                "refresh-token": refresh_token(user.id, user.username, user.email),
            }
            return Response(token, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_403_FORBIDDEN)


class UserView(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
