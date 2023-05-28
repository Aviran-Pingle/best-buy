import sys

import pyinputplus as pyip

import promotions
from store import Store
from products import Product, LimitedProduct, NonStockedProduct


def list_products(store: Store):
    """ Prints products list (only active products) """
    print("______")
    for i, product in enumerate(store.get_all_products(), start=1):
        print(f"{i}. {product}")
    print("______\n")


def print_total_quantity(store: Store):
    """ Prints the number of products in store """
    print(f"Total of {store.get_total_quantity()} items in store\n")


def order(store: Store):
    """ Receives an order from the user and calculates the cost """
    shopping_list = []
    list_products(store)
    print("When you want to finish order, enter empty text.")
    while True:
        product_num = pyip.inputInt(prompt="Which product # do you want? ",
                                    blank=True, min=1,
                                    max=len(store.get_all_products()))
        if not product_num:
            break
        product = store.get_all_products()[product_num - 1]
        maximum_amount = (None if isinstance(product, NonStockedProduct)
                          else product.quantity)
        amount = pyip.inputInt(prompt="Enter amount: ", min=1,
                               max=maximum_amount)
        shopping_list.append((product, amount))
        print("added to list")
    cost = store.order(shopping_list)
    print(f"\nOrder made, total cost: {cost}\n")


def start(store: Store):
    """ Starts the interaction with the user  """

    ops = {
        "List all products in store": list_products,
        "Show total amount in store": print_total_quantity,
        "Make an order": order,
        "Quit": lambda args: sys.exit()
    }

    while True:
        ops[pyip.inputMenu(list(ops.keys()), numbered=True)](store)


def main():
    # setup initial stock of inventory
    product_list = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250),
        NonStockedProduct("Windows License", price=125),
        LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
        ]

    # Create promotion catalog
    second_half_price = promotions.SecondHalfPrice("Second Half price!")
    third_one_free = promotions.ThirdOneFree("Third One Free!")
    thirty_percent = promotions.PercentDiscount("30% off!", percent=30)

    # Add promotions to products
    product_list[0].promotion = second_half_price
    product_list[1].promotion = third_one_free
    product_list[3].promotion = thirty_percent

    best_buy = Store(product_list)
    start(best_buy)


if __name__ == "__main__":
    main()
