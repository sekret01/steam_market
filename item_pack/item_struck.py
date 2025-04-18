

class Item:
    """ Хранение информации об уже купленном предмете """

    def __init__(
            self,
            app_id: int,
            asset_id: int,
            name: str,
            buy_price: int
    ):
        self.app_id = app_id
        self.asset_id = asset_id
        self.name = name
        self.buy_price = buy_price

    def __repr__(self) -> str:
        return f"Item {self.asset_id} [app:{self.app_id} name:{self.name}]"