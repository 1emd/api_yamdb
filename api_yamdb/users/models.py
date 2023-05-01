from django.contrib.auth.models import AbstractUser
from django.db import models

MAX_LENGTH_USERNAME = 150
MAX_LENGTH_EMAIL = 254
MAX_LENGTH_ROLE = 50
MAX_LENGTH_NAME = 150


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    )

    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=MAX_LENGTH_USERNAME,
        null=True,
        unique=True
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=MAX_LENGTH_EMAIL,
        unique=True
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=MAX_LENGTH_ROLE,
        choices=ROLES,
        null=True,
        default=USER
    )
    bio = models.TextField(
        verbose_name='О себе',
        blank=True,
        null=True
    )
    first_name = models.CharField(max_length=MAX_LENGTH_NAME, null=True)
    last_name = models.CharField(max_length=MAX_LENGTH_NAME, null=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
