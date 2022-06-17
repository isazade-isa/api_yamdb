from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES = (
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Admin'),
    )
    email = models.EmailField('email address', unique=True)
    bio = models.TextField(
        blank=True,
    )
    role = models.CharField(max_length=50, choices=ROLES, default=USER)

    def __str__(self):
        return self.username

