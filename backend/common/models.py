from django.db import models


class SortableModel(models.Model):
    """Ручной порядок: поле используют drag-and-drop списки и инлайны Unfold."""

    sort = models.PositiveIntegerField("Порядок", default=0, db_index=True)

    class Meta:
        abstract = True
        ordering = ("sort", "pk")


class ActivatableModel(models.Model):
    is_active = models.BooleanField("Показывать", default=True)

    class Meta:
        abstract = True
