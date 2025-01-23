from django.db import models
import os

def student_photo_upload_to(instance, filename):
    # Remove the extension from the original filename
    file_extension = filename.split('.')[-1]
    # Use the student's name as the filename with the original file extension
    return f"assets/train/{instance.student_name}.{file_extension}"

# Create your models here.
class tbl_student(models.Model):
    student_name = models.CharField(max_length=255)
    student_email = models.CharField(max_length=255)
    student_contact = models.CharField(max_length=255)
    student_address = models.CharField(max_length=255)
    student_password = models.CharField(max_length=255)
    student_photo = models.FileField(upload_to=student_photo_upload_to)

class Attendance(models.Model):
    name = models.CharField(max_length=100)
    time = models.TimeField()
    date = models.DateField()

    def __str__(self):
        return self.name