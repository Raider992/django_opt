from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    birthdate = models.DateField(auto_now=False, blank=True, null=True)

    def __str__(self):
        return self.username
