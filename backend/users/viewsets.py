from django.contrib.auth import login, logout
from django.middleware.csrf import get_token
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.throttling import BaseThrottle, ScopedRateThrottle

from common.viewset_mixins import EnforceCsrfMixin

from .serializers import LoginSerializer, RegisterSerializer, UserSerializer

# Анонимные действия входа: ограничены по частоте и требуют CSRF-токен
ENTRY_ACTIONS = frozenset({"login", "register"})


class AuthViewSet(EnforceCsrfMixin, viewsets.GenericViewSet):
    """Сессионная авторизация для личного кабинета."""

    serializer_class = UserSerializer
    throttle_scope = "auth"
    csrf_actions = ENTRY_ACTIONS

    def get_permissions(self) -> list[BasePermission]:
        if self.action in {"me", "logout"}:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_throttles(self) -> list[BaseThrottle]:
        if self.action in ENTRY_ACTIONS:
            return [ScopedRateThrottle()]
        return []

    @extend_schema(request=None, responses={204: None})
    @action(detail=False, methods=["get"])
    def csrf(self, request: Request) -> Response:
        """Выставляет cookie csrftoken перед POST-запросами."""
        get_token(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(request=RegisterSerializer, responses={201: UserSerializer})
    @action(detail=False, methods=["post"])
    def register(self, request: Request) -> Response:
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

    @extend_schema(request=LoginSerializer, responses={200: UserSerializer})
    @action(detail=False, methods=["post"])
    def login(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return Response(UserSerializer(user).data)

    @extend_schema(request=None, responses={204: None})
    @action(detail=False, methods=["post"])
    def logout(self, request: Request) -> Response:
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(methods=["GET"], request=None, responses={200: UserSerializer})
    @extend_schema(methods=["PATCH"], request=UserSerializer, responses={200: UserSerializer})
    @action(detail=False, methods=["get", "patch"])
    def me(self, request: Request) -> Response:
        if request.method == "PATCH":
            serializer = UserSerializer(request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        return Response(UserSerializer(request.user).data)
