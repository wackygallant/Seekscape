from django.db import models

from django.contrib.auth.models import AbstractUser
from users.user_manager import CustomUserManager

from django.contrib.auth.models import Group

class GroupProxy(Group):
    class Meta:
        proxy = True
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'
        app_label = 'users'  # forces it into the users section


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('guide', 'Guide'),
        # ('trekker', 'Trekker'),
        ('admin', 'Admin'),
    ]

    username = None
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=10, null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guide')


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_role_display()})"
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'users'