from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils import timezone
from solo.admin import SingletonModelAdmin
from unfold.admin import ModelAdmin, StackedInline, TabularInline
from unfold.decorators import display

from .models import (
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


class SocialLinkInline(TabularInline):
    model = SocialLink
    extra = 0
    ordering_field = "sort"
    hide_ordering_field = True


@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonModelAdmin, ModelAdmin):
    inlines = (SocialLinkInline,)
    fieldsets = (
        ("Магазин", {"fields": ("site_name", "logo", "welcome_text")}),
        ("Контакты", {"fields": ("phone", "email", "address")}),
        (
            "Промо-полоса над шапкой",
            {
                "fields": (
                    "promo_enabled",
                    ("promo_label", "promo_title"),
                    ("promo_highlight", "promo_text"),
                    ("promo_button_text", "promo_url"),
                )
            },
        ),
        ("Футер", {"fields": ("copyright_text", "google_play_url", "app_store_url")}),
    )


class MenuItemInline(TabularInline):
    model = MenuItem
    extra = 0
    ordering_field = "sort"
    hide_ordering_field = True


@admin.register(Menu)
class MenuAdmin(ModelAdmin):
    list_display = ("title", "placement", "items_count", "is_active")
    list_filter = ("placement", "is_active")
    inlines = (MenuItemInline,)
    ordering_field = "sort"
    hide_ordering_field = True

    @display(description="Пунктов")
    def items_count(self, obj: Menu) -> int:
        return obj.items.count()


# Какие вложенные списки нужны каждому типу блока главной
KIND_INLINES: dict[str, tuple[str, ...]] = {
    Kind.HERO: ("banners",),
    Kind.FEATURES: ("features",),
    Kind.DEALS: ("products",),
    Kind.CATEGORIES: ("categories",),
    Kind.PRODUCT_TABS: ("categories", "products", "banners"),
    Kind.BANNERS: ("banners",),
    Kind.PRODUCT_COLUMNS: ("products",),
    Kind.NEWSLETTER: (),
}


class HomeBlockProductInline(TabularInline):
    model = HomeBlockProduct
    extra = 0
    autocomplete_fields = ("product",)
    ordering_field = "sort"
    hide_ordering_field = True
    inline_key = "products"

    def get_fields(self, request: HttpRequest, obj: HomeBlock | None = None) -> list[str]:
        # Поле «Колонка» нужно только блоку «Колонки товаров»
        fields = list(super().get_fields(request, obj))
        if obj is None or obj.kind != Kind.PRODUCT_COLUMNS:
            fields.remove("group")
        return fields


class HomeBlockCategoryInline(TabularInline):
    model = HomeBlockCategory
    extra = 0
    autocomplete_fields = ("category",)
    ordering_field = "sort"
    hide_ordering_field = True
    inline_key = "categories"


class FeatureInline(TabularInline):
    model = Feature
    extra = 0
    ordering_field = "sort"
    hide_ordering_field = True
    inline_key = "features"


class BannerInline(StackedInline):
    model = Banner
    extra = 0
    ordering_field = "sort"
    hide_ordering_field = True
    inline_key = "banners"
    fields = (
        ("variant", "theme", "is_active"),
        ("eyebrow", "badge_text"),
        "title",
        "text",
        ("image", "background_color"),
        ("button_text", "url"),
        "sort",
    )


@admin.register(HomeBlock)
class HomeBlockAdmin(ModelAdmin):
    list_display = ("block", "kind_label", "content", "is_active")
    list_filter = ("kind", "is_active")
    ordering_field = "sort"
    hide_ordering_field = True
    fields = ("kind", "is_active", "title", "subtitle", "link_text", "link_url", "ends_at")
    # Поля, которые имеют смысл не для всех типов блоков (выражения Alpine.js от поля kind)
    conditional_fields = {
        "title": f"!['{Kind.HERO}', '{Kind.FEATURES}', '{Kind.BANNERS}'].includes(kind)",
        "subtitle": f"kind == '{Kind.NEWSLETTER}'",
        "link_text": f"['{Kind.DEALS}', '{Kind.PRODUCT_TABS}', '{Kind.CATEGORIES}'].includes(kind)",
        "link_url": f"['{Kind.DEALS}', '{Kind.PRODUCT_TABS}', '{Kind.CATEGORIES}'].includes(kind)",
        "ends_at": f"kind == '{Kind.DEALS}'",
    }
    all_inlines = (HomeBlockCategoryInline, HomeBlockProductInline, BannerInline, FeatureInline)

    def get_inlines(self, request: HttpRequest, obj: HomeBlock | None) -> list[type]:
        # Содержимое блока редактируется после выбора типа и первого сохранения
        if obj is None:
            return []
        keys = KIND_INLINES.get(obj.kind, ())
        return [inline for inline in self.all_inlines if inline.inline_key in keys]

    def get_queryset(self, request: HttpRequest) -> QuerySet[HomeBlock]:
        return (
            super()
            .get_queryset(request)
            .prefetch_related("block_products", "block_categories", "banners", "features")
        )

    @display(description="Блок", header=True)
    def block(self, obj: HomeBlock) -> list[object]:
        return [str(obj), obj.get_kind_display(), str(obj.sort), None]

    # Unfold выводит название из tuple, только если значение есть в карте цветов,
    # поэтому цвет задан для каждого типа
    @display(
        description="Тип",
        label={
            Kind.HERO: "primary",
            Kind.FEATURES: "info",
            Kind.DEALS: "danger",
            Kind.CATEGORIES: "info",
            Kind.PRODUCT_TABS: "primary",
            Kind.BANNERS: "warning",
            Kind.PRODUCT_COLUMNS: "primary",
            Kind.NEWSLETTER: "success",
        },
    )
    def kind_label(self, obj: HomeBlock) -> tuple[str, str]:
        return obj.kind, obj.get_kind_display()

    @display(description="Содержимое")
    def content(self, obj: HomeBlock) -> str:
        parts = [
            ("товаров", len(obj.block_products.all())),
            ("категорий", len(obj.block_categories.all())),
            ("баннеров", len(obj.banners.all())),
            ("преимуществ", len(obj.features.all())),
        ]
        summary = ", ".join(f"{count} {name}" for name, count in parts if count)
        if obj.kind == Kind.CATEGORIES and not summary:
            summary = "категории с отметкой «на главной»"
        if obj.kind == Kind.DEALS and obj.ends_at and obj.ends_at < timezone.now():
            summary = f"{summary} · таймер истёк".lstrip(" ·")
        return summary or "—"
