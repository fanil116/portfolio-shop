from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from common.models import ActivatableModel, SortableModel


class Category(SortableModel, ActivatableModel):
    name = models.CharField("Название", max_length=120)
    slug = models.SlugField("Слаг", max_length=140, unique=True)
    parent = models.ForeignKey(
        "self",
        verbose_name="Родительская категория",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="children",
    )
    image = models.ImageField("Картинка", upload_to="catalog/categories/", blank=True)
    show_on_home = models.BooleanField(
        "В блоке категорий на главной",
        default=False,
        help_text="Используется, если в блоке «Категории» не выбраны категории вручную.",
    )

    class Meta(SortableModel.Meta):
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self) -> str:
        return self.name

    def clean(self) -> None:
        # Защита от цикла: категория не может оказаться собственным предком
        ancestor = self.parent
        while ancestor is not None:
            if ancestor.pk == self.pk:
                raise ValidationError({"parent": "Категория не может быть вложена сама в себя"})
            ancestor = ancestor.parent


class Brand(SortableModel, ActivatableModel):
    name = models.CharField("Название", max_length=120)
    slug = models.SlugField("Слаг", max_length=140, unique=True)
    logo = models.ImageField("Логотип", upload_to="catalog/brands/", blank=True)
    show_on_home = models.BooleanField("В ленте брендов на главной", default=False)

    class Meta(SortableModel.Meta):
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"

    def __str__(self) -> str:
        return self.name


class Product(ActivatableModel):
    class Badge(models.TextChoices):
        NONE = "", "Нет"
        HOT = "hot", "Хит"
        SALE = "sale", "Распродажа"
        BEST_DEAL = "best_deal", "Лучшая цена"
        NEW = "new", "Новинка"

    name = models.CharField("Название", max_length=255)
    slug = models.SlugField("Слаг", max_length=280, unique=True)
    category = models.ForeignKey(
        Category, verbose_name="Категория", on_delete=models.PROTECT, related_name="products"
    )
    brand = models.ForeignKey(
        Brand,
        verbose_name="Бренд",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
    )
    image = models.ImageField("Главное фото", upload_to="catalog/products/", blank=True)
    short_description = models.TextField("Краткое описание", blank=True)
    price = models.DecimalField(
        "Цена, ₽", max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal(0))]
    )
    old_price = models.DecimalField(
        "Старая цена, ₽",
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Если больше цены — на карточке появится зачёркнутая цена и скидка.",
    )
    rating = models.DecimalField(
        "Рейтинг",
        max_digits=2,
        decimal_places=1,
        default=Decimal(0),
        validators=[MinValueValidator(Decimal(0)), MaxValueValidator(Decimal(5))],
    )
    reviews_count = models.PositiveIntegerField("Количество отзывов", default=0)
    badge = models.CharField("Метка", max_length=20, choices=Badge.choices, blank=True)
    in_stock = models.BooleanField("В наличии", default=True)
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    updated_at = models.DateTimeField("Изменён", auto_now=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.name

    def clean(self) -> None:
        if self.old_price is not None and self.price is not None and self.old_price <= self.price:
            raise ValidationError({"old_price": "Старая цена должна быть больше текущей"})

    @property
    def discount_percent(self) -> int:
        """Скидка в процентах, округлённая вниз; 0, если старой цены нет."""
        if not self.old_price or self.old_price <= self.price:
            return 0
        return int((self.old_price - self.price) * 100 // self.old_price)
