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
    average_rating = models.DecimalField(max_digits=10, decimal_places=1, default=0)
    rated_by = models.IntegerField(default=0)
    all_ratings = models.DecimalField(max_digits=20, decimal_places=1, default=0)
