from typing import Any

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError, transaction
from rest_framework import serializers

from .models import User

EMAIL_TAKEN_MESSAGE = "Пользователь с таким email уже зарегистрирован"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name")
        read_only_fields = ("id", "email")


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    class Meta:
        model = User
        fields = ("email", "password", "first_name", "last_name")

    def validate_email(self, value: str) -> str:
        email = User.objects.normalize_email(value).lower()
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError(EMAIL_TAKEN_MESSAGE)
        return email

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        validate_password(attrs["password"], user=User(**{**attrs, "password": None}))
        return attrs

    def create(self, validated_data: dict[str, Any]) -> User:
        # Параллельная регистрация с тем же email проходит validate_email у обоих запросов,
        # поэтому ловим нарушение unique-ограничения и отдаём 400, а не 500
        try:
            with transaction.atomic():
                return User.objects.create_user(**validated_data)
        except IntegrityError as error:
            raise serializers.ValidationError({"email": [EMAIL_TAKEN_MESSAGE]}) from error


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        user = authenticate(
            request=self.context.get("request"),
            email=attrs["email"].lower(),
            password=attrs["password"],
        )
        if user is None:
            msg = "Неверный email или пароль"
            raise serializers.ValidationError(msg, code="authorization")
        attrs["user"] = user
        return attrs
