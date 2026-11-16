"""Смоук-тесты админки: страницы Unfold открываются для всех разделов."""

import pytest
from django.core.management import call_command
from django.urls import reverse

from content.models import HomeBlock

pytestmark = pytest.mark.django_db

CHANGELISTS = [
    "admin:content_homeblock_changelist",
    "admin:content_menu_changelist",
    "admin:catalog_product_changelist",
    "admin:catalog_category_changelist",
    "admin:catalog_brand_changelist",
    "admin:newsletter_subscriber_changelist",
    "admin:users_user_changelist",
    "admin:auth_group_changelist",
]


@pytest.fixture
def admin_client_seeded(client, admin_user):
    call_command("seed_demo", verbosity=0)
    client.force_login(admin_user)
    return client


@pytest.mark.parametrize("url_name", CHANGELISTS)
def test_changelists_open(admin_client_seeded, url_name):
    assert admin_client_seeded.get(reverse(url_name)).status_code == 200


@pytest.mark.parametrize(
    "url_name",
    [
        "admin:content_homeblock_add",
        "admin:catalog_product_add",
        "admin:users_user_add",
        "admin:content_sitesettings_change",
    ],
)
def test_forms_open(admin_client_seeded, url_name):
    assert admin_client_seeded.get(reverse(url_name)).status_code == 200


@pytest.mark.parametrize("kind", HomeBlock.Kind.values)
def test_home_block_change_page_for_every_kind(admin_client_seeded, kind):
    block = HomeBlock.objects.create(kind=kind)
    url = reverse("admin:content_homeblock_change", args=[block.pk])
    assert admin_client_seeded.get(url).status_code == 200


def test_admin_can_create_user_by_email(admin_client_seeded):
    response = admin_client_seeded.post(
        reverse("admin:users_user_add"),
        {
            "email": "new@example.com",
            "password1": "Str0ng-pass-123",
            "password2": "Str0ng-pass-123",
        },
    )
    assert response.status_code == 302


def test_seed_demo_fills_home(client, admin_user):
    call_command("seed_demo", verbosity=0)
    blocks = client.get("/api/home/").json()["blocks"]
    assert [b["kind"] for b in blocks] == [
        "hero",
        "features",
        "deals",
        "categories",
        "product_tabs",
        "banners",
        "product_tabs",
        "banners",
        "product_columns",
        "newsletter",
    ]
    # Повторный запуск без --force ничего не дублирует
    call_command("seed_demo", verbosity=0)
    assert HomeBlock.objects.count() == len(blocks)
