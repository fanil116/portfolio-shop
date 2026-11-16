import pytest
from django.core.cache import cache
from rest_framework.test import APIClient

from users.models import User

PASSWORD = "Str0ng-pass-123"


@pytest.fixture(autouse=True)
def _clear_cache():
    # Счётчики throttling живут в кэше — сбрасываем между тестами
    cache.clear()


@pytest.fixture(autouse=True)
def _media_root(settings, tmp_path):
    # Загруженные в тестах картинки не попадают в рабочую папку media
    settings.MEDIA_ROOT = tmp_path / "media"


@pytest.fixture
def admin_user(db) -> User:
    return User.objects.create_superuser(email="admin@example.com", password=PASSWORD)


@pytest.fixture
def api_client() -> APIClient:
    # enforce_csrf_checks=True: проверяем CSRF так же, как в браузере
    return APIClient(enforce_csrf_checks=True)


@pytest.fixture
def user(db) -> User:
    return User.objects.create_user(email="user@example.com", password=PASSWORD)


def get_csrf_token(client: APIClient) -> str:
    response = client.get("/api/auth/csrf/")
    return response.cookies["csrftoken"].value
