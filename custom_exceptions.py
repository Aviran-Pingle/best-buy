class NotActiveError(Exception):
    """ indicates an attempt to buy an inactive product  """

    def __init__(self, product_name):
        message = f"{product_name} is not active"
        super().__init__(message)


class OrderLimitationError(Exception):
    """ indicates that an item passed its maximum purchases in an order """

    def __init__(self, product_name):
        message = f"{product_name} cannot be ordered again"
        super().__init__(message)
