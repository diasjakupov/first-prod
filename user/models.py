from django.db import models
from django.contrib.auth.models import AbstractUser

def DefineUserPathImages(instance, filename):
    return f'users/{instance.username}/{filename}'

class User(AbstractUser):
    gender_choices=(
        ('male', 'male'),
        ('female', 'female')
        )


    gender=models.CharField(max_length=300, choices=gender_choices, null=True, blank=True)
    image = models.ImageField(
        upload_to=DefineUserPathImages,
        null=True,
        blank=True,
        default='default/def.jpg')
    created_date=models.DateTimeField(null=True, auto_now_add=True)

    REQUIRED_FIELDS = ['gender', 'first_name']