from requests import Session
from DataBase import apps
from .order_stack import OrderStack
from .order_struct import Order


class OrderManager:
    """ Класс, управляющий заполнение стека товаров """

    def __init__(self, session: Session) -> None:
        self.stack_hub: dict[int, OrderStack] = {}
        self.session: Session = session

    def _add_stack(self, app_id: int) -> None:
        self.stack_hub[app_id] = OrderStack(app_id)

    @property
    def apps(self) -> list[int]:
        return list(self.stack_hub.keys())

    def free_count_in_stack(self, app_id: int) -> int:
        if not app_id in self.stack_hub.keys():
            self._add_stack(app_id)
        return self.stack_hub[app_id].free_count

    def orders_on_app(self, app_id: int) -> list[int]:
        return self.stack_hub[app_id].orders_list

    def filled_stacks(self) -> dict[int, bool]:
        return {app_id: stack.is_full for app_id, stack in self.stack_hub.items()}

    def book_order(self, app_id: int, count: int):
        if app_id not in self.stack_hub.keys():
            self._add_stack(app_id)
        self.stack_hub[app_id].booking(count)

    def add_order(self, order: Order) -> None:
        # if order.app_id not in self.stack_hub.keys():
        #     self._add_stack(order.app_id)
        self.stack_hub[order.app_id].add(order)

    def remove_order(self, order: Order) -> None:
        app_id = order.app_id
        if app_id not in self.stack_hub: return
        self.stack_hub[app_id].remove(order)
        if self.stack_hub[app_id].size_now == 0:
            self.stack_hub.pop(app_id)
