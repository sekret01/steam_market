from order_struct import Order


class OrderStack:
    """ Объект для хранения купленных товаров  """

    def __init__(self, app_id: int):
        self.app_id = app_id
        self._steck: list[Order] = []
        self._limit: int = 2
        self._count: int = 0

    def set_limit(self, new_limit: int) -> None:
        if new_limit < 0: self._limit = 0
        self._limit = new_limit

    def add(self, order: Order) -> None:
        if self._count < self._limit: return
        self._steck.append(order)
        self._count += 1

    def remove(self, order: Order) -> None:
        self._steck.remove(order)
        self._count -= 1

    @property
    def size_now(self) -> int:
        return self._count
