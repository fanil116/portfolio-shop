import pytest

from content.models import Menu, MenuItem, SiteSettings, SocialLink
from newsletter.models import Subscriber

from .conftest import get_csrf_token
from .factories import make_category

pytestmark = pytest.mark.django_db


def test_site_settings_and_menus(client):
    settings = SiteSettings.get_solo()
    settings.phone = "+7 800 000-00-00"
    settings.promo_enabled = True
    settings.promo_highlight = "59%"
    settings.save()
    SocialLink.objects.create(settings=settings, network="telegram", url="https://t.me/x")
    menu = Menu.objects.create(title="Шапка", placement=Menu.Placement.HEADER)
    MenuItem.objects.create(menu=menu, title="Второй", url="/b", sort=1)
    MenuItem.objects.create(menu=menu, title="Первый", url="/a", sort=0)
    Menu.objects.create(title="Скрытое", placement=Menu.Placement.FOOTER, is_active=False)

    data = client.get("/api/site/").json()

    assert data["settings"]["phone"] == "+7 800 000-00-00"
    assert data["settings"]["promo"]["highlight"] == "59%"
    assert data["settings"]["socials"] == [{"network": "telegram", "url": "https://t.me/x"}]
    assert [m["title"] for m in data["menus"]] == ["Шапка"]
    assert [i["title"] for i in data["menus"][0]["items"]] == ["Первый", "Второй"]


def test_disabled_promo_is_null(client):
    assert client.get("/api/site/").json()["settings"]["promo"] is None


def test_category_tree_skips_inactive_branches(client):
    root = make_category(name="Корень")
    make_category(name="Дочерняя", parent=root)
    hidden = make_category(name="Скрытая", is_active=False)
    make_category(name="Под скрытой", parent=hidden)

    tree = client.get("/api/catalog/categories/").json()

    assert [c["name"] for c in tree] == ["Корень"]
    assert [c["name"] for c in tree[0]["children"]] == ["Дочерняя"]


def subscribe(client, email):
    token = get_csrf_token(client)
    return client.post(
        "/api/newsletter/subscribe/", {"email": email}, format="json", HTTP_X_CSRFTOKEN=token
    )


def test_subscribe_is_idempotent(api_client):
    assert subscribe(api_client, "Fan@Example.com").status_code == 204
    assert subscribe(api_client, "fan@example.com").status_code == 204
    assert list(Subscriber.objects.values_list("email", flat=True)) == ["fan@example.com"]


def test_subscribe_requires_csrf(api_client):
    response = api_client.post("/api/newsletter/subscribe/", {"email": "a@b.ru"}, format="json")
    assert response.status_code == 403
    assert not Subscriber.objects.exists()


def test_subscribe_validates_email(api_client):
    assert subscribe(api_client, "not-an-email").status_code == 400


def test_subscribe_is_throttled(api_client):
    statuses = [subscribe(api_client, f"u{i}@example.com").status_code for i in range(6)]
    assert statuses[-1] == 429
