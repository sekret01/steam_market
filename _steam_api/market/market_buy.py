import json
from requests import Session
from .market_base import BaseMarket


class BuyMarket(BaseMarket):
    """
    Создание корректных заголовков и настроек
    для успешного прохождения запроса на покупку или
    создания запроса на покупку
    """

    def __init__(self) -> None:
        super().__init__()
        self.buy_url: str = "https://steamcommunity.com/market/createbuyorder/"
        self.cansel_url: str = "https://steamcommunity.com/market/cancelbuyorder/"
        self.base_refer: str = "https://steamcommunity.com/market/listings/"
        self.price_limit = 1000  # в копейках

    def set_price_limit(self, new_limit):
        if new_limit < 3: return
        self.price_limit = new_limit

    def buy_item(
            self,
            session: Session,
            app_id: int,
            item_name: str,
            price_for_one: int = 3,
            quantity: int = 1
    ) -> dict:
        """
    Создание лота продажи предмета
    
    :param session: (int) - request-сессия, от которой происходит запрос
    :param steam_id: (int) - id профиля steam
    :param app_id: (int) - id приложения
    :param item_name: (str) - название предмета
    :param price_for_one: (int) - цена одного предмета на продажу
    :param quantity: (int) - количество товаров
    :return: (dict) - результат запроса
    """
        if price_for_one > self.price_limit: return {"success": False, "res": f"stop operation, {price_for_one} more than price limit ({self.price_limit})"}
        old_headers = session.headers
        referer_url = self.base_refer + f"{app_id}/{item_name}"
        self.headers["Referer"] = referer_url
        session.headers.update(self.headers)
        session_id = self._get_session_id(dict(session.cookies))
        if session_id is None: return {"success": False, "res": f"no session_id in cookies"}

        request_data = {
            "sessionid": session_id,
            "currency": 5,
            "appid": app_id,
            "market_hash_name": item_name,
            "price_total": price_for_one * quantity,
            "tradefee_tax": 0,
            "quantity": quantity,
            "save_my_address": 0,
            # billing_state: None
        }
        resp = session.post(url=self.buy_url, data=request_data)
        session.headers.update(old_headers)
        return resp.json()

    def cansel_buy(self, session: Session, order_id: int) -> dict:
        session_id = self._get_session_id(dict(session.cookies))
        data = {"sessionid": session_id, "buy_orderid": order_id}
        resp = session.post(url=self.cansel_url, data=data).json()
        return resp
