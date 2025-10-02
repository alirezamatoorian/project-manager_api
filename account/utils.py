import secrets
from django.core.cache import cache


def generate_otp_code():
    return ''.join(secrets.choice("0123456789") for _ in range(5))


def store_otp(phone, otp, ttl=180):
    cache.set(phone, otp, ttl)
