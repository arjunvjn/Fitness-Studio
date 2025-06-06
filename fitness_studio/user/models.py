from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from .managers import CustomUserManager

# Create your models here.
class CustomUser(AbstractBaseUser):

    class UserRole(models.TextChoices):
        INSTRUCTOR = 'instructor'
        USER = 'user'
    
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.USER)

    USERNAME_FIELD = "email"

    objects = CustomUserManager()

    def __str__(self):
        return self.email