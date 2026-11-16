from django.db.models.fields.files import ImageFieldFile
from rest_framework import serializers

from .models import Brand, Category, Product


def image_url(image: ImageFieldFile | None) -> str | None:
    # Относительный URL: фронт и медиа живут на одном домене за nginx
    return image.url if image else None


class BrandSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    class Meta:
        model = Brand
        fields = ("id", "name", "slug", "logo")

    def get_logo(self, obj: Brand) -> str | None:
        return image_url(obj.logo)


class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "image", "parent_id")

    def get_image(self, obj: Category) -> str | None:
        return image_url(obj.image)


class CategoryTreeSerializer(CategorySerializer):
    children = serializers.SerializerMethodField()

    class Meta(CategorySerializer.Meta):
        fields = (*CategorySerializer.Meta.fields, "children")

    def get_children(self, obj: Category) -> list[dict]:
        children = self.context["children_by_parent"].get(obj.pk, [])
        return CategoryTreeSerializer(children, many=True, context=self.context).data


class ProductCardSerializer(serializers.ModelSerializer):
    """Карточка товара в списках. category_ids — категория и все её предки (для табов)."""

    image = serializers.SerializerMethodField()
    brand = serializers.CharField(source="brand.name", default=None)
    discount_percent = serializers.IntegerField(read_only=True)
    category_ids = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "slug",
            "image",
            "brand",
            "price",
            "old_price",
            "discount_percent",
            "rating",
            "reviews_count",
            "badge",
            "in_stock",
            "category_ids",
        )

    def get_image(self, obj: Product) -> str | None:
        return image_url(obj.image)

    def get_category_ids(self, obj: Product) -> list[int]:
        # Карта id → parent_id собирается одним запросом во view, здесь только обход
        parents: dict[int, int | None] = self.context.get("category_parents", {})
        ids: list[int] = []
        current: int | None = obj.category_id
        while current is not None and current not in ids:
            ids.append(current)
            current = parents.get(current)
        return ids
