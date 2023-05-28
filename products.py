import custom_exceptions
import promotions


class Product:
    """  Represents a product available in the store  """

    def __init__(self, name: str, price: float, quantity: float):
        if not name:
            raise ValueError("Name cannot be empty!")
        if price < 0 or quantity < 0:
            raise ValueError("Price/Quantity must be positive!")

        self._name = name
        self._price = price
        self._quantity = quantity
        self._active = True
        self._promotion = None

    @property
    def price(self):
        """ Getter for price """
        return self._price

    @property
    def promotion(self):
        """ Getter for promotion """
        return self._promotion

    @promotion.setter
    def promotion(self, value: promotions.Promotion):
        """ Setter for promotion """
        if not isinstance(value, promotions.Promotion):
            raise TypeError("Value should be a Promotion object")
        self._promotion = value

    def remove_promotion(self):
        """ Sets product's promotion to None """
        self._promotion = None

    @property
    def quantity(self) -> float:
        """ Getter for quantity """
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        """
        Setter for quantity
        If quantity reaches 0, deactivates the product
        """
        self._quantity = value
        if not self.quantity:
            self.deactivate()

    @property
    def active(self) -> bool:
        """
        Getter for active
        """
        return self._active

    def activate(self):
        """ Activates the product """
        self._active = True

    def deactivate(self):
        """ Deactivates the product """
        self._active = False

    def __str__(self) -> str:
        """ Returns a string that represents the product """
        desc = (f"{self._name}, Price: {self._price}, "
                f"Quantity: {self._quantity}")
        if self._promotion:
            desc += f", Promotion: {self._promotion.name}"
        return desc

    def __gt__(self, other):
        """ Checks if the product is more expensive than another product """
        return self.price > other.price

    def buy(self, quantity) -> float:
        """
        Buys a given quantity of the product
        Updates the quantity of the product
        Returns the total price (float) of the purchase
        In case of a problem raises an Exception
        """
        if not self.active:
            raise custom_exceptions.NotActiveError(self._name)

        if not 0 < quantity <= self._quantity:
            raise ValueError(
                f"{self._name}: quantity must be between 1 to {self._quantity}"
            )

        self.quantity = self.quantity - quantity

        total_price = quantity * self._price
        if self.promotion:
            return total_price - self.promotion.apply_promotion(self, quantity)
        return total_price


class NonStockedProduct(Product):
    """ Non-physical product """

    def __init__(self, name, price):
        super().__init__(name, price, quantity=float("inf"))

    def __str__(self) -> str:
        desc = f"{self._name}, Price: {self._price}"
        if self.promotion:
            desc += f", Promotion: {self._promotion.name}"
        return desc


class LimitedProduct(Product):
    """ Products that can only be purchased limited times per order """

    def __init__(self, name, price, quantity, maximum):
        super().__init__(name, price, quantity)
        self._maximum = maximum

    def __str__(self) -> str:
        return f"{super().__str__()}, Maximum: {self._maximum}"

    @property
    def name(self):
        return self._name

    @property
    def maximum(self):
        return self._maximum
