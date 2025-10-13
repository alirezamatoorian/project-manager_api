from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import UserManager
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    phone = PhoneNumberField(unique=True, region='IR')
    email = models.EmailField(blank=True, null=True)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.phone}"

    class Meta:
        ordering = ['-date_joined']
