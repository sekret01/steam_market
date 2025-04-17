import json
from requests import Session
from .market_base import BaseMarket


class SellMarket(BaseMarket):
    """
    Настройка для продажи товаров
    """

    def __init__(self):
        super().__init__()
        self.sell_url = "https://steamcommunity.com/market/sellitem/"
        self.cansel_url: str = "https://steamcommunity.com/market/removelisting/"  # "https://steamcommunity.com/market/cancelbuyorder/"
        self.base_refer: str = "https://steamcommunity.com/profiles/"  #steam_id/inventory

    def sell_item(
            self,
            session:  Session,
            steam_id: int,
            app_id: int,
            asset_id: int,
            price_for_one: int = 3,
            amount: int = 1
    ) -> dict:
        """
        Создание лота продажи предмета

        :param session: (int) - request-сессия, от которой происходит запрос
        :param steam_id: (int) - id профиля steam
        :param app_id: (int) - id приложения
        :param asset_id: (int) - id объект
        :param price_for_one: (int) - цена одного предмета на продажу
        :param amount: (int) - количество товаров
        :return: (dict) - результат запроса
        """
        if price_for_one < 3: return {"success": False, "res": f"price must be more than 2, have: {price_for_one}"}
        old_headers = session.headers
        referer_url = self.base_refer + f"{steam_id}/inventory"
        self.headers["Referer"] = referer_url
        session.headers.update(self.headers)
        session_id = self._get_session_id(dict(session.cookies))
        if session_id is None: return {"success": False, "res": f"no session_id in cookies"}
        request_data = {
            "sessionid": session_id,
            "appid": app_id,
            "contextid": 2,
            "assetid": asset_id,
            "amount": amount,
            "price": price_for_one * amount,
        }
        resp = session.post(url=self.sell_url, data=request_data).json()
        session.headers.update(old_headers)
        return resp

    def _remove_listing(self, session: Session, asset_id: int) -> dict:

        # dont work
        session_id = self._get_session_id(dict(session.cookies))
        data = {"sessionid": session_id}
        resp = session.post(url=self.cansel_url + f"{...}", data=data).json()  # какое-то число, это не app_id и asset_id
        return resp