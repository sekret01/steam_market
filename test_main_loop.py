import time

from blocker import Blocker
from _steam_api import Inventory, InventoryManager
from configs import STEAMID
from order_pack import Order, OrderManager
from item_pack import Item, ItemManager
from _results import SetsSession
from DataBase import apps
from _steam_api import BuyMarket, SellMarket
import datetime


SAVE_PATH_COOKIES = "saved_data/cookies.json"
MONITOR_APPS = [apps.TeamFortress]
BUY_PRICE = 10
SELL_PRICE = 10
ORDER_LIMIT = 5
INVENTORY_LIMIT = 10


def str_time_now() -> str:
    return datetime.datetime.now().strftime("%H:%M:%S")



def main(session: SetsSession):
    inventory = Inventory(session=session, steam_id=STEAMID, monitoring_apps=MONITOR_APPS)
    order_manager = OrderManager(session=session, steck_limit=ORDER_LIMIT)
    item_manager = ItemManager(session=session, steck_limit=INVENTORY_LIMIT)
    blocker = Blocker()
    buyer = BuyMarket()
    seller = SellMarket()
    print(f"[{str_time_now()}] \033[33m[set up]\033[0m Данные созданы и заполнены")

    while True:
        for app in MONITOR_APPS:

            # блок для обработки новых предметов
            new_items = inventory.update_items(app, get_change=True)
            if new_items:
                # print(f"найдено {len(new_items)} новых предметов: [{list(new_items.values())}]")
                for key, val in new_items.items():
                    order = order_manager.search_order(app, val['name'])
                    item = Item(app_id=int(app),
                                asset_id=int(val['assetid']),
                                name=val['name'],
                                buy_price=int(order.buy_price),  # надо запоминать цену продажи !!!
                                sell_price=SELL_PRICE)
                    item_manager.add_item(item)
                    order_manager.remove_order(order)
                    blocker.decrease_amount(item_name=val['name'])
                    print(f"[{str_time_now()}] \033[34m[new item]\033[0m заказ {order} -> предмет {item}")

                    seller.sell_item(session=session, steam_id=STEAMID, app_id=app, asset_id=item.asset_id, price_for_one=SELL_PRICE, amount=1)
                    item.set_selling()
                    # print(f"предмет {item} выставлен на продажу")

                # print(f"предметы были добавлены")



            # блок для создания новых запросов на покупку
            free_size = order_manager.free_count_in_stack(app)
            free_size_items = item_manager.free_count_in_stack(app)

            _item_name = "Scream Fortress XVI War Paint Case"  # inter 2024 Cosmetic Case || Scream Fortress XVI War Paint Case

            if free_size > 0 and free_size_items > 0 and not blocker.is_blocked(item_name=_item_name):
                # print(f"найдено {free_size} свободных мест в стеке заказов")


                rez_size = free_size if free_size < free_size_items else free_size_items
                order_manager.book_order(app, rez_size)  # free_size
                # print(f"места забронированы. \nКоличество забитых мест стека: {order_manager.stack_hub[app].size_now}\nКоличество товаров: {order_manager.stack_hub[app].fact_size_now}")

                resp = buyer.buy_item(session=session, app_id=app, item_name=_item_name, price_for_one=BUY_PRICE, quantity=rez_size) # W
                blocker.set_amount(item_name=_item_name, amount=rez_size)
                print('[{str_time_now()}] \033[37m[book stack]\033[0m success:', resp['success'])
                if resp['success'] == 1:
                    order_id = resp['buy_orderid']
                    print(f"[{str_time_now()}] \033[37m[book stack]\033[0m ID заказа: {order_id} -> ID игры:{app} количество:{rez_size}")
                elif resp['success'] == 29:
                    print(f"[{str_time_now()}] \033[37m[book stack]\033[0m " + resp['message'])
                    order_manager.book_order(app, -rez_size)
                else:
                    print(f"[{str_time_now()}] \033[37m[book stack]\033[0m " + resp['message'])
                    print(f'[{str_time_now()}] \033[37m[book stack]\033[0m отмена брони')
                    order_manager.book_order(app, -rez_size)


        # блок для обработки новых заказов
        new_buy_items = inventory.update_buys(get_change=True)
        if new_buy_items:
            print(f"[{str_time_now()}] \033[36m[new order]\033[0m заказ {list(new_buy_items.keys())} найден")
            for key, val in new_buy_items.items():
                for _ in range(int(val['quantity'])):
                    order = Order(app_id=int(val['appid']),
                                  order_id=int(key),
                                  buy_price=int(val['price']),
                                  name=val['name'])
                    order_manager.add_order(order)
                    print(f"[{str_time_now()}] \033[36m[new order]\033[0m заказ [ID игры:{val['appid']} цена:{round(int(val['price']) / 100, 2)} предмет:{val['name']}]")

        # блок обработки проданных предметов
        selling_items = inventory.update_sells(get_change=True)
        if selling_items or len(item_manager.item_hub) > 0:

            selling_ids = [int(key) for key in selling_items.keys()]
            deleted_items = []

            for app, stack in item_manager.item_hub.items():
                ids = item_manager.get_ids(app_id=app)
                for _id in ids:
                    if _id in selling_ids:
                        item = item_manager.search_item_by_assetid(assetid=_id)
                        if item is None: print(f"ERROR: {_id} not in list")
                        deleted_items.append(item)
            for it in deleted_items:
                print(f'[{str_time_now()}] \033[32m[buy item]\033[0m удален из списка предметов: {it} -> {round(it.sell_price / 100, 2)} руб')
                item_manager.remove_item(it)



        # print(f"бронировано заказов: {order_manager.stack_hub[440].size_now}")
        # print(f"в наличии заказов: {order_manager.stack_hub[440]._count} / {order_manager.stack_hub[440]._limit}")
        # print(f"количество предметов: {item_manager.item_hub[440]._count} / {item_manager.item_hub[440]._limit}")
        # print(f"блокировки предметов: {blocker.items}")
        #
        # print('-'*30)

        time.sleep(5)

        # необходимо создать стек для предметов (ItemStack) и управляющий им элемент
        # при заполнении стека ItemStack новые продажи не будут осуществляться -> новые заказы не будут оформляться
        # из-за недостатка места








if __name__ == "__main__":
    sess = SetsSession()
    sess.update_cookies("saved_data/cookies.json")
    sess.update_headers("_results/input_default_data/headers_default.json")
    try:
        main(sess)
    except KeyboardInterrupt:
        print("stop working...")
        sess.save_cookies(SAVE_PATH_COOKIES)
