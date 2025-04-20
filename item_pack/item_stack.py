from .item_struck import Item


class ItemStack:
    """ Стек для хранения предметов (уже купленных) """
    def __init__(self, app_id: int) -> None:
        self.app_id = app_id
        self._stack: list[Item] = []
        self._limit: int = 4
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
            self._count -= 1

    def search_item(self, app_id: int, name: str) -> Item | None:
        for item in self._stack:
            if item.name == name and item.app_id == app_id:
                return item
        return None

    def search_item_by_assetid(self, assetid: int) -> Item | None:
        for item in self._stack:
            if item.asset_id == assetid:
                return item
        return None


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

