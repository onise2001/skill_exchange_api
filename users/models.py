from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('Administrator', "administrator"),
        ('Tutor', "tutor"),
        ('Student', "student"),
    )

    role = models.CharField(max_length=100, choices=ROLE_CHOICES)