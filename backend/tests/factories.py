from decimal import Decimal
from itertools import count

from catalog.models import Brand, Category, Product
from content.models import HomeBlock, HomeBlockProduct

_seq = count(1)


def make_category(**kwargs) -> Category:
    n = next(_seq)
    return Category.objects.create(**{"name": f"Категория {n}", "slug": f"cat-{n}", **kwargs})


def make_brand(**kwargs) -> Brand:
    n = next(_seq)
    return Brand.objects.create(**{"name": f"Бренд {n}", "slug": f"brand-{n}", **kwargs})


def make_product(category: Category | None = None, **kwargs) -> Product:
    n = next(_seq)
    return Product.objects.create(
        **{
            "name": f"Товар {n}",
            "slug": f"product-{n}",
            "category": category or make_category(),
            "price": Decimal(1000),
            **kwargs,
        }
    )


def make_block(kind: str, products: list[Product] = (), **kwargs) -> HomeBlock:
    block = HomeBlock.objects.create(kind=kind, **kwargs)
    for sort, product in enumerate(products):
        HomeBlockProduct.objects.create(block=block, product=product, sort=sort)
    return block
