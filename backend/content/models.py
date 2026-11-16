from django.core.validators import RegexValidator
from django.db import models
from solo.models import SingletonModel

from catalog.models import Category, Product
from common.models import ActivatableModel, SortableModel

hex_color_validator = RegexValidator(r"^#[0-9a-fA-F]{6}$", "Цвет в формате #RRGGBB")


class SiteSettings(SingletonModel):
    """Общие настройки сайта: шапка, промо-полоса, контакты, футер."""

    site_name = models.CharField("Название магазина", max_length=80, default="Clicon")
    logo = models.ImageField("Логотип", upload_to="content/", blank=True)
    welcome_text = models.CharField("Приветствие в верхней строке", max_length=160, blank=True)
    phone = models.CharField("Телефон", max_length=40, blank=True)
    email = models.EmailField("Email", blank=True)
    address = models.TextField("Адрес", blank=True)
    copyright_text = models.CharField("Копирайт в футере", max_length=200, blank=True)
    google_play_url = models.URLField("Ссылка на Google Play", blank=True)
    app_store_url = models.URLField("Ссылка на App Store", blank=True)

    promo_enabled = models.BooleanField("Показывать промо-полосу", default=False)
    promo_label = models.CharField(
        "Плашка", max_length=30, blank=True, help_text="Например, «Black»"
    )
    promo_title = models.CharField("Заголовок", max_length=60, blank=True)
    promo_highlight = models.CharField(
        "Акцент", max_length=30, blank=True, help_text="Например, «59%»"
    )
    promo_text = models.CharField("Текст после акцента", max_length=60, blank=True)
    promo_button_text = models.CharField("Текст кнопки", max_length=40, blank=True)
    promo_url = models.CharField("Ссылка кнопки", max_length=255, blank=True)

    class Meta:
        verbose_name = "Настройки сайта"

    def __str__(self) -> str:
        return "Настройки сайта"


class SocialLink(SortableModel):
    class Network(models.TextChoices):
        TELEGRAM = "telegram", "Telegram"
        VK = "vk", "ВКонтакте"
        YOUTUBE = "youtube", "YouTube"
        X = "x", "X (Twitter)"
        FACEBOOK = "facebook", "Facebook"
        INSTAGRAM = "instagram", "Instagram"
        PINTEREST = "pinterest", "Pinterest"
        REDDIT = "reddit", "Reddit"

    settings = models.ForeignKey(SiteSettings, on_delete=models.CASCADE, related_name="socials")
    network = models.CharField("Соцсеть", max_length=20, choices=Network.choices)
    url = models.URLField("Ссылка")

    class Meta(SortableModel.Meta):
        verbose_name = "Соцсеть"
        verbose_name_plural = "Соцсети"

    def __str__(self) -> str:
        return self.get_network_display()


class Menu(SortableModel, ActivatableModel):
    class Placement(models.TextChoices):
        HEADER = "header", "Шапка: быстрые ссылки"
        FOOTER = "footer", "Футер: колонка ссылок"
        FOOTER_TAGS = "footer_tags", "Футер: популярные теги"

    title = models.CharField("Заголовок", max_length=80)
    placement = models.CharField("Где выводится", max_length=20, choices=Placement.choices)

    class Meta(SortableModel.Meta):
        verbose_name = "Меню"
        verbose_name_plural = "Меню"

    def __str__(self) -> str:
        return f"{self.title} ({self.get_placement_display()})"


class MenuItem(SortableModel):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="items")
    title = models.CharField("Текст", max_length=80)
    url = models.CharField("Ссылка", max_length=255)
    icon = models.CharField(
        "Иконка", max_length=40, blank=True, help_text="Имя иконки из набора фронтенда"
    )

    class Meta(SortableModel.Meta):
        verbose_name = "Пункт меню"
        verbose_name_plural = "Пункты меню"

    def __str__(self) -> str:
        return self.title


class HomeBlock(SortableModel, ActivatableModel):
    """Секция главной страницы. Порядок секций на сайте = порядок в админке."""

    class Kind(models.TextChoices):
        HERO = "hero", "Слайдер с баннерами"
        FEATURES = "features", "Преимущества"
        DEALS = "deals", "Лучшие предложения с таймером"
        CATEGORIES = "categories", "Категории"
        PRODUCT_TABS = "product_tabs", "Товары с табами по категориям"
        BANNERS = "banners", "Баннеры"
        PRODUCT_COLUMNS = "product_columns", "Колонки товаров"
        NEWSLETTER = "newsletter", "Подписка и бренды"

    kind = models.CharField("Тип блока", max_length=30, choices=Kind.choices)
    title = models.CharField("Заголовок", max_length=120, blank=True)
    subtitle = models.TextField("Подзаголовок", blank=True)
    link_text = models.CharField("Текст ссылки", max_length=60, blank=True)
    link_url = models.CharField("Ссылка", max_length=255, blank=True)
    ends_at = models.DateTimeField(
        "Акция до", null=True, blank=True, help_text="Таймер обратного отсчёта"
    )

    class Meta(SortableModel.Meta):
        verbose_name = "Блок главной"
        verbose_name_plural = "Блоки главной"

    def __str__(self) -> str:
        return self.title or self.get_kind_display()


class HomeBlockProduct(SortableModel):
    block = models.ForeignKey(HomeBlock, on_delete=models.CASCADE, related_name="block_products")
    product = models.ForeignKey(Product, verbose_name="Товар", on_delete=models.CASCADE)
    group = models.CharField(
        "Колонка",
        max_length=60,
        blank=True,
        help_text="Только для «Колонок товаров»: товары с одинаковым названием колонки "
        "выводятся вместе (например, «Хиты продаж»).",
    )

    class Meta(SortableModel.Meta):
        verbose_name = "Товар блока"
        verbose_name_plural = "Товары блока"

    def __str__(self) -> str:
        return str(self.product)


class HomeBlockCategory(SortableModel):
    block = models.ForeignKey(HomeBlock, on_delete=models.CASCADE, related_name="block_categories")
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE)

    class Meta(SortableModel.Meta):
        verbose_name = "Категория блока"
        verbose_name_plural = "Категории блока"

    def __str__(self) -> str:
        return str(self.category)


class Feature(SortableModel, ActivatableModel):
    class Icon(models.TextChoices):
        DELIVERY = "delivery", "Доставка"
        RETURN = "return", "Возврат"
        PAYMENT = "payment", "Оплата"
        SUPPORT = "support", "Поддержка"

    block = models.ForeignKey(HomeBlock, on_delete=models.CASCADE, related_name="features")
    icon = models.CharField("Иконка", max_length=20, choices=Icon.choices)
    title = models.CharField("Заголовок", max_length=60)
    text = models.CharField("Текст", max_length=120, blank=True)

    class Meta(SortableModel.Meta):
        verbose_name = "Преимущество"
        verbose_name_plural = "Преимущества"

    def __str__(self) -> str:
        return self.title


class Banner(SortableModel, ActivatableModel):
    class Variant(models.TextChoices):
        CARD = "card", "Карточка"
        SLIDE = "slide", "Слайд (в слайдере)"
        SIDE = "side", "Боковой"

    class Theme(models.TextChoices):
        LIGHT = "light", "Светлый (тёмный текст)"
        DARK = "dark", "Тёмный (светлый текст)"

    block = models.ForeignKey(HomeBlock, on_delete=models.CASCADE, related_name="banners")
    variant = models.CharField("Вид", max_length=10, choices=Variant.choices, default=Variant.CARD)
    eyebrow = models.CharField("Надзаголовок", max_length=60, blank=True)
    title = models.CharField("Заголовок", max_length=120)
    text = models.TextField("Текст", blank=True)
    badge_text = models.CharField(
        "Плашка", max_length=30, blank=True, help_text="Например, «29% OFF» или «$299»"
    )
    image = models.ImageField("Картинка", upload_to="content/banners/", blank=True)
    background_color = models.CharField(
        "Цвет фона", max_length=7, default="#F2F4F5", validators=[hex_color_validator]
    )
    theme = models.CharField("Тема", max_length=10, choices=Theme.choices, default=Theme.LIGHT)
    button_text = models.CharField("Текст кнопки", max_length=40, blank=True)
    url = models.CharField("Ссылка", max_length=255, blank=True)

    class Meta(SortableModel.Meta):
        verbose_name = "Баннер"
        verbose_name_plural = "Баннеры"

    def __str__(self) -> str:
        return self.title
