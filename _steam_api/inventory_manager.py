from __future__ import annotations
from requests import Session
from ._url_bilder import UrlBuilder


class InventoryManager:
    """
    Объект для взаимодействия с инвентарем пользователя
    """
    def __init__(self, steam_id: int) -> None:
        self.inventory_url_base: str = f"https://steamcommunity.com/inventory/{steam_id}"  # /app_id
        self.sells_list_url_base: str = "https://steamcommunity.com/market/mylistings"
        self.suffix_steam_inventory: str = "753/6?l=russian"  # &count=1000
        self.suffix_app_inventory: str = "2?l=russian"

    def get_app_items(self, session: Session, app_id: int = 753) -> dict:
        """ Получения имеющихся предметов для приложения """
        builder = UrlBuilder(self.inventory_url_base, injson=False)
        builder.add_root(app_id)
        builder.add_root(6) if app_id == 753 else builder.add_root(2)
        builder.add_parameters({'l': 'russian'})
        url = builder.get_url()
        resp = session.get(url=url).json()
        return resp

    def get_selling_items(self, session: Session, app_id: int | None = None) -> dict:
        """ Получение информации о лотах продажи """
        builder = UrlBuilder(self.sells_list_url_base)
        resp = session.get(builder.get_url()).json()  # ['success', 'pagesize', 'total_count', 'assets', 'start', 'num_active_listings', 'listings', 'listings_on_hold', 'listings_to_confirm', 'buy_orders']
        # print(resp.keys())
        return resp
