from .order_struct import Order


class OrderStack:
    """ Объект для хранения купленных товаров  """

    def __init__(self, app_id: int):
        self.app_id = app_id
        self._stack: list[Order] = []
        self._limit: int = 10
        self._count: int = 0
        self._booked: int = 0

    def set_limit(self, new_limit: int) -> None:
        if new_limit < 0: self._limit = 0
        self._limit = new_limit

    def booking(self, count: int):
        if self._booked + count > self._limit: return
        self._booked += count

    def add(self, order: Order) -> None:
        if self._count == self._limit: return
        self._stack.append(order)
        self._count += 1

    def remove(self, order: Order) -> None:
        self._stack.remove(order)
        self._count -= 1
        self._booked -= 1

    @property
    def size_now(self) -> int:
        return self._booked

    @property
    def fact_size_now(self):
        return self._count

    @property
    def is_full(self):
        return self._limit == self._booked

    @property
    def orders_list(self) -> list[int]:
        return [order.order_id for order in self._stack]

    @property
    def free_count(self):
        return self._limit - self._booked
