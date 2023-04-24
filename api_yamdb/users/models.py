from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLES = (
        ('user', 'user'),
        ('moderator', 'user'),
        ('admin', 'admin'),
    )

    username = models.CharField(max_length=100, null=True, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, choices=ROLES, null=True)
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.username
