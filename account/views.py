from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from .utils import generate_otp_code, store_otp, delete_otp
from rest_framework_simplejwt.tokens import RefreshToken
from .throttles import SendOtpThrottle


# Create your views here.


class SendOtpView(APIView):
    throttle_classes = [SendOtpThrottle]

    def post(self, request, *args, **kwargs):
        serializer = SendOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        otp = generate_otp_code()
        store_otp(phone, otp, ttl=180)
        print(f"OTP for {phone} is {otp}")
        return Response({"message": "OTP sent successfully!"}, status=200)


class VerifyOtpView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = VerifyOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data["phone"]
        user, created = User.objects.get_or_create(phone=phone)
        delete_otp(phone)
        refresh = RefreshToken.for_user(user)
        return Response({
            "user_id": user.id,
            'created': created,
            'refresh': str(refresh),
            'access': str(refresh.access_token)})


class ProfileView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
