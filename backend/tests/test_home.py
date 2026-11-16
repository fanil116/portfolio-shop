from datetime import timedelta
from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone

from content.models import Banner, Feature, HomeBlock, HomeBlockCategory

from .factories import make_block, make_brand, make_category, make_product

pytestmark = pytest.mark.django_db
Kind = HomeBlock.Kind


def get_blocks(client) -> list[dict]:
    response = client.get("/api/home/")
    assert response.status_code == 200
    return response.json()["blocks"]


def test_blocks_follow_admin_order_and_hide_inactive(client):
    product = make_product()
    make_block(Kind.DEALS, [product], title="Второй", sort=2)
    make_block(Kind.PRODUCT_TABS, [product], title="Первый", sort=1)
    make_block(Kind.DEALS, [product], title="Скрытый", sort=0, is_active=False)

    assert [b["title"] for b in get_blocks(client)] == ["Первый", "Второй"]


def test_empty_blocks_are_not_returned(client):
    make_block(Kind.DEALS, [], title="Пусто")
    make_block(Kind.DEALS, [make_product(is_active=False)], title="Только скрытые товары")
    HomeBlock.objects.create(kind=Kind.BANNERS)
    HomeBlock.objects.create(kind=Kind.NEWSLETTER, title="Подписка")

    assert [b["title"] for b in get_blocks(client)] == ["Подписка"]


def test_product_card_fields_and_category_ancestors(client):
    parent = make_category()
    child = make_category(parent=parent)
    product = make_product(
        category=child,
        brand=make_brand(name="Sony"),
        price=Decimal(750),
        old_price=Decimal(1000),
        badge="hot",
    )
    make_block(Kind.PRODUCT_TABS, [product])

    card = get_blocks(client)[0]["products"][0]
    assert card["brand"] == "Sony"
    assert card["discount_percent"] == 25
    assert card["category_ids"] == [child.pk, parent.pk]
    assert card["badge"] == "hot"
    assert card["group"] == ""


def test_expired_deal_timer_is_hidden(client):
    product = make_product()
    make_block(Kind.DEALS, [product], title="Идёт", ends_at=timezone.now() + timedelta(hours=1))
    make_block(Kind.DEALS, [product], title="Прошла", ends_at=timezone.now() - timedelta(hours=1))

    blocks = {b["title"]: b for b in get_blocks(client)}
    assert blocks["Идёт"]["ends_at"] is not None
    assert blocks["Прошла"]["ends_at"] is None


def test_categories_block_falls_back_to_show_on_home(client):
    make_category(name="На главной", show_on_home=True)
    make_category(name="Не на главной")
    HomeBlock.objects.create(kind=Kind.CATEGORIES)

    assert [c["name"] for c in get_blocks(client)[0]["categories"]] == ["На главной"]


def test_categories_block_uses_manual_selection_in_order(client):
    first, second = make_category(name="A"), make_category(name="B", show_on_home=True)
    block = HomeBlock.objects.create(kind=Kind.CATEGORIES)
    HomeBlockCategory.objects.create(block=block, category=second, sort=0)
    HomeBlockCategory.objects.create(block=block, category=first, sort=1)

    assert [c["name"] for c in get_blocks(client)[0]["categories"]] == ["B", "A"]


def test_banners_features_and_newsletter_brands(client):
    hero = HomeBlock.objects.create(kind=Kind.HERO, sort=0)
    Banner.objects.create(block=hero, title="Видимый", sort=1)
    Banner.objects.create(block=hero, title="Скрытый", is_active=False)
    features = HomeBlock.objects.create(kind=Kind.FEATURES, sort=1)
    Feature.objects.create(block=features, icon="delivery", title="Доставка")
    make_brand(name="В ленте", show_on_home=True)
    make_brand(name="Не в ленте")
    HomeBlock.objects.create(kind=Kind.NEWSLETTER, sort=2)

    hero_data, features_data, newsletter = get_blocks(client)
    assert [b["title"] for b in hero_data["banners"]] == ["Видимый"]
    assert features_data["features"][0]["icon"] == "delivery"
    assert [b["name"] for b in newsletter["brands"]] == ["В ленте"]


def test_home_query_count_does_not_grow_with_blocks(client, django_assert_max_num_queries):
    category = make_category(show_on_home=True)
    for index in range(6):
        products = [make_product(category=category, brand=make_brand()) for _ in range(4)]
        block = make_block(Kind.PRODUCT_TABS, products, sort=index)
        HomeBlockCategory.objects.create(block=block, category=category)
        Banner.objects.create(block=block, title="Баннер")
    HomeBlock.objects.create(kind=Kind.CATEGORIES)
    HomeBlock.objects.create(kind=Kind.NEWSLETTER)

    with django_assert_max_num_queries(10):
        assert len(get_blocks(client)) == 8


def test_product_old_price_must_exceed_price():
    product = make_product(price=Decimal(1000))
    product.old_price = Decimal(900)
    with pytest.raises(ValidationError):
        product.full_clean()


def test_category_cannot_be_its_own_ancestor():
    parent = make_category()
    child = make_category(parent=parent)
    parent.parent = child
    with pytest.raises(ValidationError):
        parent.full_clean()
