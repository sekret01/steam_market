

class Blocker:
    """
    Класс для блокировки запроса на покупку предмета
    при наличии другого запроса на этот эе товар
    """

    def __init__(self):
        self.items: dict[str, int] = {}

    def set_amount(self, item_name: str, amount: int):
        self.items[item_name] = amount

    def is_blocked(self, item_name: str):
        return self.items.setdefault(item_name, 0)

    def decrease_amount(self, item_name: str, amount: int = 1):
        self.items[item_name] -= amount
