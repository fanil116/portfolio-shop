from django.utils import timezone
from rest_framework import serializers

from catalog.serializers import (
    BrandSerializer,
    CategorySerializer,
    ProductCardSerializer,
    image_url,
)

from .models import Banner, Feature, HomeBlock, HomeBlockProduct, Menu, MenuItem, SiteSettings


class BannerSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Banner
        fields = (
            "id",
            "variant",
            "eyebrow",
            "title",
            "text",
            "badge_text",
            "image",
            "background_color",
            "theme",
            "button_text",
            "url",
        )

    def get_image(self, obj: Banner) -> str | None:
        return image_url(obj.image)


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ("id", "icon", "title", "text")


class BlockProductSerializer(ProductCardSerializer):
    """Товар внутри блока: карточка + название колонки (для «Колонок товаров»)."""

    def to_representation(self, instance: HomeBlockProduct) -> dict:
        data = super().to_representation(instance.product)
        data["group"] = instance.group
        return data


class HomeBlockSerializer(serializers.ModelSerializer):
    ends_at = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    banners = BannerSerializer(many=True)
    features = FeatureSerializer(many=True)
    brands = serializers.SerializerMethodField()

    class Meta:
        model = HomeBlock
        fields = (
            "id",
            "kind",
            "title",
            "subtitle",
            "link_text",
            "link_url",
            "ends_at",
            "products",
            "categories",
            "banners",
            "features",
            "brands",
        )

    def get_ends_at(self, obj: HomeBlock) -> str | None:
        # Истёкший таймер не показываем
        if obj.ends_at and obj.ends_at > timezone.now():
            return obj.ends_at.isoformat()
        return None

    def get_products(self, obj: HomeBlock) -> list[dict]:
        return BlockProductSerializer(
            obj.block_products.all(), many=True, context=self.context
        ).data

    def get_categories(self, obj: HomeBlock) -> list[dict]:
        categories = [item.category for item in obj.block_categories.all()]
        if not categories and obj.kind == HomeBlock.Kind.CATEGORIES:
            categories = self.context["home_categories"]
        return CategorySerializer(categories, many=True).data

    def get_brands(self, obj: HomeBlock) -> list[dict]:
        if obj.kind != HomeBlock.Kind.NEWSLETTER:
            return []
        return BrandSerializer(self.context["home_brands"], many=True).data


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ("id", "title", "url", "icon")


class MenuSerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True)

    class Meta:
        model = Menu
        fields = ("id", "title", "placement", "items")


class SiteSettingsSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    socials = serializers.SerializerMethodField()
    promo = serializers.SerializerMethodField()

    class Meta:
        model = SiteSettings
        fields = (
            "site_name",
            "logo",
            "welcome_text",
            "phone",
            "email",
            "address",
            "copyright_text",
            "google_play_url",
            "app_store_url",
            "promo",
            "socials",
        )

    def get_logo(self, obj: SiteSettings) -> str | None:
        return image_url(obj.logo)

    def get_socials(self, obj: SiteSettings) -> list[dict]:
        return [{"network": link.network, "url": link.url} for link in obj.socials.all()]

    def get_promo(self, obj: SiteSettings) -> dict | None:
        if not obj.promo_enabled:
            return None
        return {
            "label": obj.promo_label,
            "title": obj.promo_title,
            "highlight": obj.promo_highlight,
            "text": obj.promo_text,
            "button_text": obj.promo_button_text,
            "url": obj.promo_url,
        }
