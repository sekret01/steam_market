from .item_struck import Item
from .item_stack import ItemStack
from requests import Session


class ItemManager:
    """
    Класс, управляющий стеками предметов,
    добавлением и удалением новых стеков и предметов
    """
    def __init__(self, session: Session):
        self.item_hub: dict[int, ItemStack] = {}
        self.session: Session = session

    def _add_stack(self, app_id) -> None:
        self.item_hub[app_id] = ItemStack(app_id)

    def add_item(self, item: Item):
        if item.app_id not in self.item_hub.keys():
            self._add_stack(item.app_id)
        self.item_hub[item.app_id].add(item)

    def remove_item(self, item: Item) -> None:
        if item.app_id not in self.item_hub.keys(): return
        self.item_hub[item.app_id].remove(item)
        if self.item_hub[item.app_id].size_now == 0:
            ...
            # self.item_hub.pop(item.app_id)

    def free_count_in_stack(self, app_id: int) -> int:
        if app_id not in self.item_hub.keys():
            self._add_stack(app_id)
        return self.item_hub[app_id].free_count

    def search_item(self, app_id: int, name: str):
        if app_id not in self.item_hub.keys(): return None
        return self.item_hub[app_id].search_item(app_id, name)

    def search_item_by_assetid(self, assetid: int):
        for stack in self.item_hub.values():
            if not (item := stack.search_item_by_assetid(assetid)) is None:
                return item

    def get_ids(self, app_id: int) -> list[int]:
        if app_id not in self.item_hub.keys(): return []
        return [int(item.asset_id) for item in self.item_hub[app_id].item_list]
