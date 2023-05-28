from abc import ABC, abstractmethod


class Promotion(ABC):
    """ Abstract class representing a product's promotion / discount """
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @staticmethod
    @abstractmethod
    def apply_promotion(product, quantity: float) -> float:
        """ Returns the discounted price after promotion was applied """
        pass


class SecondHalfPrice(Promotion):
    """ Represents a promotion where every second item is half priced """
    @staticmethod
    def apply_promotion(product, quantity) -> float:
        discounted_items = quantity // 2
        return discounted_items * product.price * 0.5


class ThirdOneFree(Promotion):
    """ Represents a promotion where every third item is free """
    @staticmethod
    def apply_promotion(product, quantity) -> float:
        free_items = quantity // 3
        return free_items * product.price


class PercentDiscount(Promotion):
    """ Represents a promotion where every item is discounted
     by a given percent"""
    def __init__(self, name, percent):
        super().__init__(name)
        self._percent = percent

    def apply_promotion(self, product, quantity) -> float:
        return product.price * quantity * self._percent * 0.01


