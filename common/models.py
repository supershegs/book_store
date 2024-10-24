from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    
    ROLE_CHOICES = [
        (USER, 'User'),
        (ADMIN, 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ADMIN)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"



class Publisher(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

