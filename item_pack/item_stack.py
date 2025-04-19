from item_struck import Item


class ItemStack:
    """ Стек для хранения предметов (уже купленных) """
    def __init__(self, app_id: int) -> None:
        self.app_id = app_id
        self._stack: list[Item] = []
        self._limit: int = 10
        self._count: int = 0

    def set_limit(self, new_limit) -> None:
        self._limit = new_limit

    def add(self, item: Item) -> None:
        if self._count == self._limit: return
        self._stack.append(item)
        self._count += 1

    def remove(self, item: Item) -> None:
        if item in self._stack:
            self._stack.remove(item)

    @property
    def free_count(self) -> int:
        return self._limit - self._count

    @property
    def is_full(self) -> bool:
        return self._limit == self._count

    @property
    def item_list(self) -> list[Item]:
        return self._stack

    @property
    def size_now(self):
        return self._count
