"""Демо-наполнение магазина и главной страницы по структуре макета Clicon.

Картинки — сгенерированные плейсхолдеры (цветной фон + подпись), без сторонних фото.
"""

import io
import random
from datetime import timedelta
from decimal import Decimal
from typing import Any

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction
from django.utils import timezone
from PIL import Image, ImageDraw

from catalog.models import Brand, Category, Product
from content.models import (
    Banner,
    Feature,
    HomeBlock,
    HomeBlockCategory,
    HomeBlockProduct,
    Menu,
    MenuItem,
    SiteSettings,
    SocialLink,
)

Kind = HomeBlock.Kind

CATEGORIES = [
    ("Компьютеры и ноутбуки", "computers", "#DCE7F3"),
    ("Смартфоны", "smartphones", "#F3E5DC"),
    ("Наушники", "headphones", "#E3F3DC"),
    ("Аксессуары", "accessories", "#F3F0DC"),
    ("Фото и видео", "cameras", "#EBDCF3"),
    ("Телевизоры", "tv", "#DCF3F1"),
    ("Бытовая техника", "appliances", "#F3DCE4"),
]
SUBCATEGORIES = [
    ("Клавиатуры и мыши", "keyboards", "accessories"),
    ("Веб-камеры", "webcams", "accessories"),
    ("Принтеры", "printers", "accessories"),
]
# Сколько первых брендов показывать в ленте на главной
BRANDS_ON_HOME = 5
BRANDS = ["Samsung", "Xiaomi", "Apple", "Sony", "LG", "Philips", "Toshiba", "Huawei"]
PRODUCTS = [
    ("Игровая приставка X5 1 ТБ", "computers", "Sony"),
    ("Ноутбук Air 13 M2 16/512 ГБ", "computers", "Apple"),
    ('Монитор 27" 4K IPS', "computers", "LG"),
    ('Моноблок 24" i5 16/512 ГБ', "computers", "Huawei"),
    ("Смартфон Galaxy S25 8/256 ГБ", "smartphones", "Samsung"),
    ("Смартфон Redmi Note 14 Pro", "smartphones", "Xiaomi"),
    ("Смартфон iPhone 16 128 ГБ", "smartphones", "Apple"),
    ("Смартфон Pura 70 12/512 ГБ", "smartphones", "Huawei"),
    ("Наушники WH-1000XM5", "headphones", "Sony"),
    ("Наушники Buds 3 Pro", "headphones", "Samsung"),
    ("Наушники AirPods Pro 2", "headphones", "Apple"),
    ("Наушники Redmi Buds 6", "headphones", "Xiaomi"),
    ("Клавиатура механическая RGB", "keyboards", "Xiaomi"),
    ("Мышь беспроводная тихая", "keyboards", "Philips"),
    ("Веб-камера Full HD", "webcams", "Philips"),
    ("Принтер лазерный Wi-Fi", "printers", "Toshiba"),
    ("Беззеркальная камера α7 IV", "cameras", "Sony"),
    ("Экшн-камера 4K", "cameras", "Xiaomi"),
    ('Телевизор 55" OLED', "tv", "LG"),
    ('Телевизор 65" QLED', "tv", "Samsung"),
    ('Телевизор 43" Smart TV', "tv", "Xiaomi"),
    ("Холодильник No Frost 2 м", "appliances", "LG"),
    ("Стиральная машина 8 кг", "appliances", "Samsung"),
    ("Робот-пылесос с влажной уборкой", "appliances", "Xiaomi"),
]


def placeholder(label: str, color: str, size: tuple[int, int] = (480, 480)) -> ContentFile:
    image = Image.new("RGB", size, color)
    draw = ImageDraw.Draw(image)
    draw.rectangle((24, 24, size[0] - 24, size[1] - 24), outline="#191C1F", width=3)
    draw.text((40, size[1] // 2), label[:40], fill="#191C1F")
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return ContentFile(buffer.getvalue())


class Command(BaseCommand):
    help = "Заполняет каталог и главную демо-данными (только если главная ещё пустая)."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--force",
            action="store_true",
            help="Удалить блоки главной, меню, товары, бренды и категории и создать заново",
        )

    @transaction.atomic
    def handle(self, *args: Any, **options: Any) -> None:
        if HomeBlock.objects.exists() and not options["force"]:
            self.stdout.write("Главная уже заполнена — пропускаю (используйте --force)")
            return
        if options["force"]:
            HomeBlock.objects.all().delete()
            Menu.objects.all().delete()
            Product.objects.all().delete()
            Brand.objects.all().delete()
            Category.objects.filter(parent__isnull=False).delete()
            Category.objects.all().delete()

        rng = random.Random(42)  # noqa: S311 — детерминированные демо-данные, не криптография
        categories = self._categories()
        brands = self._brands()
        products = self._products(categories, brands, rng)
        self._site_settings()
        self._menus()
        self._home(categories, products)
        self.stdout.write(self.style.SUCCESS(f"Готово: {len(products)} товаров, блоки главной"))

    def _categories(self) -> dict[str, Category]:
        result: dict[str, Category] = {}
        for sort, (name, slug, color) in enumerate(CATEGORIES):
            category = Category(name=name, slug=slug, sort=sort, show_on_home=True)
            category.image.save(f"{slug}.png", placeholder(name, color), save=False)
            category.save()
            result[slug] = category
        for sort, (name, slug, parent) in enumerate(SUBCATEGORIES):
            result[slug] = Category.objects.create(
                name=name, slug=slug, parent=result[parent], sort=sort
            )
        return result

    def _brands(self) -> dict[str, Brand]:
        result: dict[str, Brand] = {}
        for sort, name in enumerate(BRANDS):
            brand = Brand(
                name=name, slug=name.lower(), sort=sort, show_on_home=sort < BRANDS_ON_HOME
            )
            brand.logo.save(
                f"{brand.slug}.png", placeholder(name, "#FFFFFF", (240, 80)), save=False
            )
            brand.save()
            result[name] = brand
        return result

    def _products(
        self, categories: dict[str, Category], brands: dict[str, Brand], rng: random.Random
    ) -> list[Product]:
        badges = [*Product.Badge.values, "", "", ""]
        products = []
        for index, (name, category_slug, brand_name) in enumerate(PRODUCTS):
            price = Decimal(rng.randrange(2_990, 189_990, 1_000))
            has_discount = index % 3 == 0
            product = Product(
                name=name,
                slug=f"demo-{index + 1}",
                category=categories[category_slug],
                brand=brands[brand_name],
                short_description="Демо-товар для наполнения витрины.",
                price=price,
                old_price=(price * Decimal("1.25")).quantize(Decimal(1)) if has_discount else None,
                rating=Decimal(rng.randint(30, 50)) / 10,
                reviews_count=rng.randint(0, 900),
                badge=rng.choice(badges),
            )
            product.image.save(f"{product.slug}.png", placeholder(name, "#F2F4F5"), save=False)
            product.save()
            products.append(product)
        return products

    def _site_settings(self) -> None:
        settings = SiteSettings.get_solo()
        settings.site_name = "Clicon"
        settings.welcome_text = "Добро пожаловать в интернет-магазин электроники"
        settings.phone = "+7 (800) 555-01-04"
        settings.email = "info@example.com"
        settings.address = "Москва, ул. Примерная, 1"
        settings.copyright_text = "Демо-магазин. Дизайн: Clicon by Templatecookie (CC BY 4.0)"
        settings.promo_enabled = True
        settings.promo_label = "Black"
        settings.promo_title = "Friday"
        settings.promo_highlight = "59%"
        settings.promo_text = "скидки"
        settings.promo_button_text = "В магазин"
        settings.promo_url = "/catalog"
        settings.save()
        settings.socials.all().delete()
        for sort, network in enumerate(["telegram", "vk", "youtube"]):
            SocialLink.objects.create(
                settings=settings, network=network, url=f"https://example.com/{network}", sort=sort
            )

    def _menus(self) -> None:
        menus = [
            (
                "Быстрые ссылки",
                Menu.Placement.HEADER,
                [
                    ("Отследить заказ", "/track-order", "location"),
                    ("Сравнение", "/compare", "compare"),
                    ("Поддержка", "/support", "headphones"),
                    ("Помощь", "/faq", "info"),
                ],
            ),
            (
                "Покупателям",
                Menu.Placement.FOOTER,
                [
                    ("Каталог", "/catalog", ""),
                    ("Корзина", "/cart", ""),
                    ("Избранное", "/wishlist", ""),
                    ("Отследить заказ", "/track-order", ""),
                ],
            ),
            (
                "Популярные теги",
                Menu.Placement.FOOTER_TAGS,
                [(tag, f"/catalog?q={tag}", "") for tag in ["Игры", "iPhone", "ТВ", "Наушники"]],
            ),
        ]
        for sort, (title, placement, items) in enumerate(menus):
            menu = Menu.objects.create(title=title, placement=placement, sort=sort)
            MenuItem.objects.bulk_create(
                MenuItem(menu=menu, title=t, url=u, icon=i, sort=s)
                for s, (t, u, i) in enumerate(items)
            )

    def _home(self, categories: dict[str, Category], products: list[Product]) -> None:
        sort = iter(range(100))

        hero = HomeBlock.objects.create(kind=Kind.HERO, sort=next(sort))
        Banner.objects.bulk_create(
            [
                Banner(
                    block=hero,
                    variant=Banner.Variant.SLIDE,
                    eyebrow="Лучшее для игр",
                    title="Игровые приставки",
                    text="Три месяца подписки в подарок при покупке до конца месяца.",
                    badge_text="49 990 ₽",
                    button_text="Купить",
                    url="/catalog/computers",
                    sort=0,
                ),
                Banner(
                    block=hero,
                    variant=Banner.Variant.SIDE,
                    eyebrow="Летняя распродажа",
                    title="Смартфоны с камерой 50 Мп",
                    badge_text="−29%",
                    background_color="#191C1F",
                    theme=Banner.Theme.DARK,
                    button_text="Купить",
                    url="/catalog/smartphones",
                    sort=1,
                ),
                Banner(
                    block=hero,
                    variant=Banner.Variant.SIDE,
                    title="Беспроводные наушники",
                    badge_text="9 990 ₽",
                    button_text="Купить",
                    url="/catalog/headphones",
                    sort=2,
                ),
            ]
        )

        features = HomeBlock.objects.create(kind=Kind.FEATURES, sort=next(sort))
        Feature.objects.bulk_create(
            Feature(block=features, icon=icon, title=title, text=text, sort=index)
            for index, (icon, title, text) in enumerate(
                [
                    ("delivery", "Быстрая доставка", "1–3 дня по России"),
                    ("return", "Возврат 14 дней", "Без лишних вопросов"),
                    ("payment", "Безопасная оплата", "Деньги защищены"),
                    ("support", "Поддержка 24/7", "Ответим в чате"),
                ]
            )
        )

        deals = HomeBlock.objects.create(
            kind=Kind.DEALS,
            title="Лучшие предложения",
            link_text="Все товары",
            link_url="/catalog",
            ends_at=timezone.now() + timedelta(days=3),
            sort=next(sort),
        )
        self._attach_products(deals, products[:9])

        HomeBlock.objects.create(
            kind=Kind.CATEGORIES, title="Покупайте по категориям", sort=next(sort)
        )

        featured = HomeBlock.objects.create(
            kind=Kind.PRODUCT_TABS,
            title="Рекомендуем",
            link_text="Все товары",
            link_url="/catalog",
            sort=next(sort),
        )
        self._attach_categories(
            featured, [categories[s] for s in ("smartphones", "computers", "headphones", "tv")]
        )
        self._attach_products(featured, products[:24:3] + products[1:24:3])
        Banner.objects.create(
            block=featured,
            variant=Banner.Variant.SIDE,
            eyebrow="Компьютеры и аксессуары",
            title="Скидка 32%",
            text="На всю электронику",
            background_color="#F3DE6D",
            button_text="В магазин",
            url="/catalog",
        )

        promo = HomeBlock.objects.create(kind=Kind.BANNERS, sort=next(sort))
        Banner.objects.bulk_create(
            [
                Banner(
                    block=promo,
                    eyebrow="Новинка",
                    title="Умная колонка mini",
                    text="Звук, который заполняет комнату.",
                    button_text="Купить",
                    url="/catalog/headphones",
                    sort=0,
                ),
                Banner(
                    block=promo,
                    eyebrow="Новинка",
                    title="Смартфон 12/256 ГБ",
                    badge_text="39 990 ₽",
                    background_color="#191C1F",
                    theme=Banner.Theme.DARK,
                    button_text="Купить",
                    url="/catalog/smartphones",
                    sort=1,
                ),
            ]
        )

        accessories = HomeBlock.objects.create(
            kind=Kind.PRODUCT_TABS,
            title="Аксессуары для компьютера",
            link_text="Все товары",
            link_url="/catalog/accessories",
            sort=next(sort),
        )
        self._attach_categories(
            accessories, [categories[s] for s in ("keyboards", "webcams", "printers")]
        )
        self._attach_products(accessories, [p for p in products if p.category.parent_id])

        wide = HomeBlock.objects.create(kind=Kind.BANNERS, sort=next(sort))
        Banner.objects.create(
            block=wide,
            eyebrow="Скидка до 20 000 ₽",
            title="Ноутбук Air 13",
            text="Чип нового поколения, 16 ГБ памяти, 512 ГБ SSD.",
            badge_text="119 990 ₽",
            background_color="#FFE7D6",
            button_text="Купить",
            url="/catalog/computers",
        )

        columns = HomeBlock.objects.create(kind=Kind.PRODUCT_COLUMNS, sort=next(sort))
        for group_index, group in enumerate(["Распродажа дня", "Хиты продаж", "Высокий рейтинг"]):
            self._attach_products(columns, products[group_index * 3 : group_index * 3 + 3], group)
        self._attach_products(columns, products[-3:], "Новинки")

        HomeBlock.objects.create(
            kind=Kind.NEWSLETTER,
            title="Подпишитесь на рассылку",
            subtitle="Скидки, новинки и подборки — раз в неделю, без спама.",
            sort=next(sort),
        )

        for banner in Banner.objects.filter(image=""):
            banner.image.save(f"banner-{banner.pk}.png", placeholder(banner.title, "#E4E7E9"))

    @staticmethod
    def _attach_products(block: HomeBlock, products: list[Product], group: str = "") -> None:
        start = block.block_products.count()
        HomeBlockProduct.objects.bulk_create(
            HomeBlockProduct(block=block, product=product, group=group, sort=start + index)
            for index, product in enumerate(products)
        )

    @staticmethod
    def _attach_categories(block: HomeBlock, categories: list[Category]) -> None:
        HomeBlockCategory.objects.bulk_create(
            HomeBlockCategory(block=block, category=category, sort=index)
            for index, category in enumerate(categories)
        )
