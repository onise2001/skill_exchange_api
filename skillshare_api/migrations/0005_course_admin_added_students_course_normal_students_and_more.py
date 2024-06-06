# Generated by Django 5.0.6 on 2024-05-30 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skillshare_api', '0004_course_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='admin_added_students',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='course',
            name='normal_students',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='admin_added',
            field=models.BooleanField(default=False),
        ),
    ]