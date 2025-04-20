from _steam_api import BuyMarket, SellMarket
from _steam_api import Inventory
from _results import SetsSession
from configs import STEAMID

SESSION = SetsSession()
SESSION.update_headers("_results/input_default_data/headers_default.json")
SESSION.update_cookies("saved_data/cookies.json")


def sell_items():


    app_id = 440
    name = "Winter 2024 Cosmetic Case"

    seller = SellMarket()
    data = Inventory(SESSION, STEAMID, [app_id]).items[app_id]
    for key, val in data.items():
        if val['name'] == name:
            seller.sell_item(SESSION, STEAMID, app_id, val['assetid'], price_for_one=5, amount=1)


if __name__ == "__main__":
    sell_items()
