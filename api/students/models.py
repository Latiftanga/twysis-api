import os
import uuid
from django.db import models
from django.contrib.auth import get_user_model

from core.models import School, House, Class


def student_image_file_path(instance, filename):
    """Generate file path for new recipe image"""
    ext = filename.split('.')[-1]  # [-1] returns the last item from a list
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/students/', filename)


class Guardian(models.Model):
    """Student guardian object"""
    name = models.CharField(max_length=255)
    relation = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=255, blank=True)
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='guardians'
    )
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    """Student object model"""
    SEX_CHOICES = (('M', 'Male'), ('F', 'Female'))
    STATUS_CHOICES = (('Boarding', 'Boarding'), ('Day', 'Day'))

    admission_id = models.CharField(max_length=128, unique=True, blank=True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    status = models.CharField(max_length=40, choices=STATUS_CHOICES)
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=255)
    residential_address = models.CharField(max_length=255)
    hometown = models.CharField(max_length=255)
    nationality = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=255, blank=True)
    grade_class = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        related_name='students',
        blank=True,
        null=True
    )
    house = models.ForeignKey(
        House,
        related_name='students',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='students',
    )
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    guardians = models.ManyToManyField(
        'Guardian',
        related_name='students',
        blank=True,
    )
    image = models.ImageField(
        blank=True,
        null=True,
        upload_to=student_image_file_path
    )
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    @property
    def name(self):
        return f'{self.last_name} {self.first_name}'

    def __str__(self):
        return self.name
