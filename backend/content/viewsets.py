from django.db.models import Prefetch, QuerySet
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from catalog.models import Brand, Category

from .models import (
    Banner,
    Feature,
    HomeBlock,
    HomeBlockCategory,
    HomeBlockProduct,
    Menu,
    SiteSettings,
)
from .serializers import HomeBlockSerializer, MenuSerializer, SiteSettingsSerializer

Kind = HomeBlock.Kind


def home_blocks_queryset() -> QuerySet[HomeBlock]:
    """Активные блоки со всем содержимым — фиксированное число запросов на любое число блоков."""
    return HomeBlock.objects.filter(is_active=True).prefetch_related(
        Prefetch(
            "block_products",
            queryset=HomeBlockProduct.objects.filter(product__is_active=True).select_related(
                "product__brand"
            ),
        ),
        Prefetch(
            "block_categories",
            queryset=HomeBlockCategory.objects.filter(category__is_active=True).select_related(
                "category"
            ),
        ),
        Prefetch("banners", queryset=Banner.objects.filter(is_active=True)),
        Prefetch("features", queryset=Feature.objects.filter(is_active=True)),
    )


def has_content(block: HomeBlock, context: dict) -> bool:
    """Блок без содержимого на сайт не отдаём, чтобы не было пустых секций."""
    products = block.block_products.all()
    banners = block.banners.all()
    checks = {
        Kind.HERO: bool(banners),
        Kind.FEATURES: bool(block.features.all()),
        Kind.DEALS: bool(products),
        Kind.CATEGORIES: bool(block.block_categories.all() or context["home_categories"]),
        Kind.PRODUCT_TABS: bool(products),
        Kind.BANNERS: bool(banners),
        Kind.PRODUCT_COLUMNS: bool(products),
        Kind.NEWSLETTER: True,
    }
    return checks.get(block.kind, False)


class HomeViewSet(viewsets.ViewSet):
    """Содержимое главной страницы: блоки в порядке из админки."""

    @extend_schema(
        responses={
            200: inline_serializer("Home", {"blocks": HomeBlockSerializer(many=True)}),
        }
    )
    def list(self, request: Request) -> Response:
        blocks = list(home_blocks_queryset())
        kinds = {block.kind for block in blocks}
        context = {
            "request": request,
            # Для табов: product.category_ids включает предков категории
            "category_parents": dict(Category.objects.values_list("id", "parent_id")),
            "home_categories": (
                list(Category.objects.filter(is_active=True, show_on_home=True))
                if Kind.CATEGORIES in kinds
                else []
            ),
            "home_brands": (
                list(Brand.objects.filter(is_active=True, show_on_home=True))
                if Kind.NEWSLETTER in kinds
                else []
            ),
        }
        visible = [block for block in blocks if has_content(block, context)]
        return Response({"blocks": HomeBlockSerializer(visible, many=True, context=context).data})


class SiteViewSet(viewsets.ViewSet):
    """Настройки сайта и меню для шапки и футера."""

    @extend_schema(
        responses={
            200: inline_serializer(
                "Site",
                {
                    "settings": SiteSettingsSerializer(),
                    "menus": MenuSerializer(many=True),
                },
            ),
        }
    )
    def list(self, request: Request) -> Response:
        settings = SiteSettings.get_solo()
        menus = Menu.objects.filter(is_active=True).prefetch_related("items")
        return Response(
            {
                "settings": SiteSettingsSerializer(settings).data,
                "menus": MenuSerializer(menus, many=True).data,
            }
        )
