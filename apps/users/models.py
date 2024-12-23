from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser, UserManager

from .managers import UserManager

class User(AbstractUser):
    username = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(unique=True)

    # TODO Adicionar foto de usuário padrão
    profile_picture = models.ImageField(upload_to='user/image/profile_pictures/', blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    objects = UserManager()

    def __str__(self) -> str:
        return self.email