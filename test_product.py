import pytest

from products import Product


@pytest.fixture
def product():
    return Product("MacBook Air M2", price=1450, quantity=100)


def test_normal_product_creation(product):
    assert type(product) is Product


def test_invalid_name():
    with pytest.raises(ValueError):
        Product("", price=1450, quantity=100)


def test_invalid_price():
    with pytest.raises(ValueError):
        Product("MacBook Air M2", price=-1450, quantity=100)


def test_inactivation(product):
    product.quantity = 0
    assert not product.active


def test_quantity_update_after_buy(product):
    starting_quantity = product.quantity
    product.buy(1)
    assert product.quantity == starting_quantity - 1


def test_exceed_quantity(product):
    with pytest.raises(ValueError):
        product.buy(product.quantity + 1)
