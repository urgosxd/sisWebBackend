from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .managers import CustomUserManager

class CustomUser(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length = 16,unique=True,null=False ,blank=False)
    email = models.EmailField("Direccion de Email",unique=True)
    is_staff =models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now())

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['username','email']
    objects = CustomUserManager()
    def __str__(self):
        return self.username



