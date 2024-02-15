from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=255)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    class Meta:
        managed = False
        db_table = settings.USERS_TABLE


User.objects = User.objects.using("auth_db")