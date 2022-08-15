from django.db import models
from django.contrib.auth.models import AbstractUser
import re
# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.IntegerField(null=True)

 