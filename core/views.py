from .models import User
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import RegisterSerializer,UserSerializer
from rest_framework.permissions import IsAdminUser,IsAuthenticated

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message" : "user create successfully."},status=status.HTTP_201_CREATED)


class UserView(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]

