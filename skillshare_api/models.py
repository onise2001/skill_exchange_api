from django.db import models
from users.models import CustomUser 
# Create your models here.

class Enrollment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    enrolled_on = models.DateField(auto_now_add=True)



class Review(models.Model):
    text = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reviewed_at = models.DateTimeField(auto_now_add=True)



# Add 5 point rating system, pagination and filters
class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    tutor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    days = models.TextField()
    max_students = models.IntegerField()
    current_students = models.IntegerField(default=0)
    students = models.ManyToManyField(Enrollment,default=[])
    reviews = models.ManyToManyField(Review,default=[])




