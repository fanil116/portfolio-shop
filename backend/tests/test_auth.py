import pytest
from rest_framework.exceptions import ValidationError

from users.models import User
from users.serializers import RegisterSerializer

from .conftest import PASSWORD, get_csrf_token

pytestmark = pytest.mark.django_db


def post(client, url, data=None):
    token = get_csrf_token(client)
    return client.post(url, data or {}, format="json", HTTP_X_CSRFTOKEN=token)


def test_csrf_sets_cookie(api_client):
    response = api_client.get("/api/auth/csrf/")
    assert response.status_code == 204
    assert "csrftoken" in response.cookies


@pytest.mark.parametrize(
    "url", ["/api/auth/login/", "/api/auth/register/"], ids=["login", "register"]
)
def test_anonymous_post_without_csrf_is_rejected(api_client, user, url):
    response = api_client.post(
        url, {"email": "other@example.com", "password": PASSWORD}, format="json"
    )
    assert response.status_code == 403
    assert not User.objects.filter(email="other@example.com").exists()


def test_authenticated_patch_without_csrf_is_rejected(api_client, user):
    post(api_client, "/api/auth/login/", {"email": user.email, "password": PASSWORD})
    response = api_client.patch("/api/auth/me/", {"first_name": "X"}, format="json")
    assert response.status_code == 403


def test_register_creates_user_and_logs_in(api_client):
    response = post(
        api_client,
        "/api/auth/register/",
        {"email": "New@Example.com", "password": PASSWORD, "first_name": "Иван"},
    )
    assert response.status_code == 201
    assert response.data["email"] == "new@example.com"
    assert User.objects.filter(email="new@example.com").exists()

    me = api_client.get("/api/auth/me/")
    assert me.status_code == 200
    assert me.data["first_name"] == "Иван"


def test_register_rejects_duplicate_email(api_client, user):
    response = post(
        api_client, "/api/auth/register/", {"email": "USER@example.com", "password": PASSWORD}
    )
    assert response.status_code == 400
    assert "email" in response.data


def test_register_race_on_same_email_returns_validation_error(user):
    # Имитирует второй параллельный запрос: validate_email уже пройден, а пользователь создан
    serializer = RegisterSerializer()
    with pytest.raises(ValidationError) as exc_info:
        serializer.create({"email": user.email, "password": PASSWORD})
    assert "email" in exc_info.value.detail


def test_register_rejects_weak_password(api_client):
    response = post(
        api_client, "/api/auth/register/", {"email": "weak@example.com", "password": "123"}
    )
    assert response.status_code == 400
    assert not User.objects.filter(email="weak@example.com").exists()


def test_login_and_me(api_client, user):
    response = post(
        api_client, "/api/auth/login/", {"email": "USER@example.com", "password": PASSWORD}
    )
    assert response.status_code == 200
    assert response.data["email"] == user.email

    me = api_client.get("/api/auth/me/")
    assert me.status_code == 200
    assert me.data["id"] == user.id


def test_login_wrong_password(api_client, user):
    response = post(api_client, "/api/auth/login/", {"email": user.email, "password": "wrong"})
    assert response.status_code == 400


def test_me_requires_auth(api_client):
    assert api_client.get("/api/auth/me/").status_code == 403


def test_me_patch_updates_profile_but_not_email(api_client, user):
    api_client.force_authenticate(user)
    response = api_client.patch(
        "/api/auth/me/", {"first_name": "Пётр", "email": "hack@example.com"}, format="json"
    )
    assert response.status_code == 200
    user.refresh_from_db()
    assert user.first_name == "Пётр"
    assert user.email == "user@example.com"


def test_logout(api_client, user):
    post(api_client, "/api/auth/login/", {"email": user.email, "password": PASSWORD})
    response = post(api_client, "/api/auth/logout/")
    assert response.status_code == 204
    assert api_client.get("/api/auth/me/").status_code == 403


def test_login_is_throttled(api_client, user):
    statuses = [
        post(api_client, "/api/auth/login/", {"email": user.email, "password": "wrong"}).status_code
        for _ in range(11)
    ]
    assert statuses[-1] == 429


def test_unknown_host_is_rejected(client, db):
    assert client.get("/healthcheck/", HTTP_HOST="evil.example").status_code == 400


def test_healthcheck(client, db):
    response = client.get("/healthcheck/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
