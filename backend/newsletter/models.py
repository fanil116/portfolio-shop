from django.db import models


class Subscriber(models.Model):
    email = models.EmailField("Email", unique=True)
    created_at = models.DateTimeField("Подписался", auto_now_add=True)

    class Meta:
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.email
