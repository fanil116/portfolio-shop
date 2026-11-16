from collections import defaultdict

from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Category
from .serializers import CategoryTreeSerializer


class CategoryViewSet(viewsets.ViewSet):
    """Дерево активных категорий для меню каталога."""

    @extend_schema(responses={200: CategoryTreeSerializer(many=True)})
    def list(self, request: Request) -> Response:
        categories = list(Category.objects.filter(is_active=True))
        active_ids = {category.pk for category in categories}
        children_by_parent: dict[int | None, list[Category]] = defaultdict(list)
        for category in categories:
            # Ветка под скрытым родителем тоже скрыта
            if category.parent_id is None or category.parent_id in active_ids:
                children_by_parent[category.parent_id].append(category)
        serializer = CategoryTreeSerializer(
            children_by_parent.get(None, []),
            many=True,
            context={"children_by_parent": children_by_parent},
        )
        return Response(serializer.data)
