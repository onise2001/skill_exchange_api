from django.db import models
from users.models import CustomUser 
from django.db.models.signals import pre_save
from django.dispatch import receiver
# Create your models here.





class Enrollment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    enrolled_on = models.DateField(auto_now_add=True)
    admin_added = models.BooleanField(default=False)



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
    available = models.BooleanField(default=True)
    admin_added_students = models.IntegerField(default=0)
    normal_students = models.IntegerField(default=0)




class TutorEnrollment(models.Model):
    tutor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tutor')
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='student')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)





@receiver(pre_save, sender=Course)
def set_availability(sender, instance, **kwargs):
    if instance.max_students == instance.normal_students:
        instance.available = False
    else:
        instance.available = True




