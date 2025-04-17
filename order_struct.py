# import time
import datetime

class Order:
    """ Структура хранения основной информации о единице товара """

    def __init__(
            self,
            app_id: int,
            item_id: int,
            order_id: int,
            buy_price: int,
            sell_price: int,
            name: str = ""
    ) -> None:
        self.app_id = app_id
        self.item_id = item_id
        self.order_id = order_id
        self.buy_price = buy_price
        self.sell_price = sell_price
        self.name = name
        self.create_time = datetime.datetime.now()

    def __repr__(self) -> str:
        return f"order [{self.order_id} -- app:{self.app_id} item:{self.item_id} name:{self.name}]"

    def wait_time(self) -> dict[str,int]:
        res = datetime.datetime.now() - self.create_time
        days = res.days
        sec = res.seconds
        return {"days": days, "seconds": sec}
