from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle

from common.viewset_mixins import EnforceCsrfMixin

from .models import Subscriber


class SubscribeSerializer(serializers.Serializer):
    email = serializers.EmailField()


class NewsletterViewSet(EnforceCsrfMixin, viewsets.GenericViewSet):
    serializer_class = SubscribeSerializer
    throttle_classes = (ScopedRateThrottle,)
    throttle_scope = "newsletter"
    csrf_actions = frozenset({"subscribe"})

    @extend_schema(request=SubscribeSerializer, responses={204: None})
    @action(detail=False, methods=["post"])
    def subscribe(self, request: Request) -> Response:
        serializer = SubscribeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Повторная подписка — не ошибка; ответ одинаковый, чтобы не раскрывать, кто подписан
        Subscriber.objects.get_or_create(email=serializer.validated_data["email"].lower())
        return Response(status=status.HTTP_204_NO_CONTENT)
