from rest_framework import serializers
import re
from .models import User
from rest_framework.response import Response


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

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('a user with this email exists')
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


class Login(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        return email, password


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class ResendChangedEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField(max_length=1000)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']



def check():
    print("hook")