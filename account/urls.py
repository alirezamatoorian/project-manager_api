from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

app_name = 'account'

urlpatterns = [
    path('send-otp/', views.SendOtpView.as_view(), name='send-otp'),
    path('verify-otp/', views.VerifyOtpView.as_view(), name='verify-otp'),
    path('refresh_token/', TokenRefreshView.as_view(), name='refresh-token'),
    path('profile/', views.ProfileView.as_view(), name='profile')

]
