from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from user.models import User

#serializer to validate and sign up new user
class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'username']

    username = serializers.CharField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True, required=True
    )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            password=make_password(validated_data['password'])
        )
        return user


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password")

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)