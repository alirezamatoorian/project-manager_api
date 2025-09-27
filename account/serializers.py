from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .utils import generate_otp_code
from django.core.cache import cache

User = get_user_model()


class SendOtpSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11)



class RegisterSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['phone', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('پسورد و تکرار پسورد با هم یکی نیستند!!!')
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['phone', 'email', 'first_name', 'last_name']
        read_only_fields = ['phone']
