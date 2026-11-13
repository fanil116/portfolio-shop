from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db import models

from ..querysets import UserManager


class User(AbstractUser):
    """Пользователь: вход по email."""

    username = None
    email = models.EmailField("Email", unique=True)

    objects: ClassVar[UserManager] = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: ClassVar[list[str]] = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self) -> str:
        return self.email
