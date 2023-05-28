from typing import List, Tuple

from products import Product, LimitedProduct
from custom_exceptions import NotActiveError, OrderLimitationError


class Store:
    """  Hold products, allow the user to make a purchase """

    def __init__(self, products: List[Product]):
        self._products = products

    def __contains__(self, item):
        """ Checks if a product exists in the store """
        return item in self._products

    def __add__(self, other):
        """ Combines two stores, returns a new instance """
        return Store(self.get_all_products() + other.get_all_products())

    def add_product(self, product: Product):
        """ Adds product to the store. """
        self._products.append(product)

    def remove_product(self, product: Product):
        """ Removes a product from store. """
        self._products.remove(product)

    def get_total_quantity(self) -> int:
        """ Returns how many items are in the store in total """
        return sum([product.quantity for product in self._products])

    def get_all_products(self) -> List[Product]:
        """ Returns all products in the store that are active """
        return [product for product in self._products if product.active]

    @staticmethod
    def order(shopping_list: List[Tuple[Product, int]]) -> float:
        """
        Gets a list of tuples, where each tuple has 2 items:
        Product (Product class) and quantity (int).
        Buys the products and returns the total price of the order, if there is
        an error with a certain purchase it prints the error and continues
        to the next one.
        """
        total_cost = 0
        prev_purchases = {}
        for product, quantity in shopping_list:
            try:
                Store._check_limitation(product, prev_purchases, quantity)
                total_cost += product.buy(quantity)
            except (ValueError, NotActiveError, OrderLimitationError) as e:
                print(e)
        return total_cost

    @staticmethod
    def _check_limitation(product, prev_purchases, amount):
        """ Checks if a product reached its purchases threshold """
        if isinstance(product, LimitedProduct):
            ordered = prev_purchases.get(product.name, 0)
            if product.maximum < amount or ordered == product.maximum:
                raise OrderLimitationError(product.name)
            else:
                prev_purchases[product.name] = ordered + amount
