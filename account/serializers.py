from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.cache import cache
from phonenumber_field.serializerfields import PhoneNumberField

User = get_user_model()


class SendOtpSerializer(serializers.Serializer):
    phone = PhoneNumberField(region='IR')


class VerifyOtpSerializer(serializers.Serializer):
    phone = PhoneNumberField(region='IR')
    code = serializers.CharField(max_length=5)

    def validate(self, attrs):
        phone = str(attrs['phone'])
        code = attrs['code']

        stored_code = cache.get(phone)
        if not stored_code:
            raise serializers.ValidationError("otp expired or invalid")
        if stored_code != code:
            raise serializers.ValidationError("invalid otp")
        return attrs


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['phone', 'email', 'first_name', 'last_name']
        read_only_fields = ['phone']
