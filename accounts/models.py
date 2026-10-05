from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    USERNAME_FIELD = 'username'
    email = models.EmailField(unique=True)
    pass
