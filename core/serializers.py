from rest_framework import serializers
import re
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'phone', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_phone(self, value):
        regex = "^(\+98|0)?9\d{9}$"
        if not re.match(regex, str(value)):
            raise serializers.ValidationError("phone number is not currect.")
        return value

    def save(self, **kwargs):
        user = User(
            username=self.validated_data['username'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            email=self.validated_data['email'],
            phone=self.validated_data['phone']
        )
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
