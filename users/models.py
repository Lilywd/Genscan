from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import MyUserManager


class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
 
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

    objects = MyUserManager()

    def __str__(self):
        return self.username

    