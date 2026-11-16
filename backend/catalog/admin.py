from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import RangeNumericFilter
from unfold.decorators import display

from common.admin import header_with_image

from .models import Brand, Category, Product


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ("header", "parent", "show_on_home", "is_active")
    list_filter = ("is_active", "show_on_home", "parent")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ("parent",)
    ordering_field = "sort"
    hide_ordering_field = True

    @display(description="Категория", header=True)
    def header(self, obj: Category) -> list[object]:
        return header_with_image(obj.name, obj.slug, obj.image)


@admin.register(Brand)
class BrandAdmin(ModelAdmin):
    list_display = ("header", "show_on_home", "is_active")
    list_filter = ("is_active", "show_on_home")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    ordering_field = "sort"
    hide_ordering_field = True

    @display(description="Бренд", header=True)
    def header(self, obj: Brand) -> list[object]:
        return header_with_image(obj.name, obj.slug, obj.logo)


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ("header", "category", "brand", "price", "discount", "badge_label", "is_active")
    list_filter = (
        "is_active",
        "in_stock",
        "badge",
        "category",
        "brand",
        ("price", RangeNumericFilter),
    )
    list_filter_submit = True
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ("category", "brand")
    list_select_related = ("category", "brand")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("name", "slug", "category", "brand", "image", "short_description")}),
        ("Цена и наличие", {"fields": ("price", "old_price", "in_stock")}),
        ("Витрина", {"fields": ("badge", "rating", "reviews_count", "is_active")}),
        ("Служебное", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    )

    @display(description="Товар", header=True)
    def header(self, obj: Product) -> list[object]:
        return header_with_image(obj.name, obj.slug, obj.image)

    @display(description="Скидка")
    def discount(self, obj: Product) -> str:
        return f"−{obj.discount_percent}%" if obj.discount_percent else "—"

    @display(
        description="Метка",
        label={
            Product.Badge.HOT: "danger",
            Product.Badge.SALE: "success",
            Product.Badge.BEST_DEAL: "info",
            Product.Badge.NEW: "warning",
        },
    )
    def badge_label(self, obj: Product) -> tuple[str, str] | str:
        return (obj.badge, obj.get_badge_display()) if obj.badge else "—"
