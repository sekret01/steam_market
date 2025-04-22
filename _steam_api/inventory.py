from requests import Session
from .inventory_manager import InventoryManager


class Inventory:
    """
    Хранение предметов в инвентаре, предметов на продажу
    и их обновление

    Хранение предметов осуществляется в следующем формате

    *items*
        {appid: {assetid: {assetid, classid, name}}}

    *sell_items*
        {id: {id, appid, classid, name}}

    *buy_items*
        {buy_orderid: buy_orderid, appid, name, price, quantity, quantity_remaining}
    """

    def __init__(self, session: Session, steam_id: int, monitoring_apps: list[int]):
        self.session: Session = session
        self.inv_m = InventoryManager(steam_id)
        self.steam_id: int = steam_id
        self.items: dict = {}
        self.sell_list: dict = {}
        self.buy_list: dict = {}

        for app in monitoring_apps:
            self.update_items(app)
        self.update_sells()
        self.update_buys()

    def update_items(self, app_id: int, get_change: bool = False) -> dict | None:
        resp_data = self.inv_m.get_app_items(session=self.session, app_id=app_id)
        if resp_data is None: return
        items_data: list[dict] = resp_data.get('assets')
        items_descriptions: list[dict] = resp_data.get('descriptions')
        if items_data is None: return
        res_data = {}
        res_description = {}
        return_data = None

        for item in items_descriptions:
            res_description[item['classid']] = item['name']

        for item_d in items_data:
            res_data[item_d['assetid']] = {'assetid': item_d['assetid'], 'classid': item_d['classid'], 'name': res_description[item_d['classid']]}

        old_data: dict | None = self.items.setdefault(app_id)
        if get_change:
            return_data = {}
            if old_data is None: return_data = res_data
            else:
                for asset_id in res_data.keys():
                    if asset_id not in old_data.keys():
                        return_data[asset_id] = res_data[asset_id]
        self.items[app_id] = res_data
        return return_data

    def update_sells(self, get_change: bool = False) -> dict | None:
        resp_data = self.inv_m.get_selling_items(self.session)
        return_data = None
        res_data = {}

        # обработка списка продаваемых
        if not (sell_list := resp_data.get('assets')) is None:
            for app in sell_list.keys():
                app_data = sell_list[app].get('2')
                for key, val in app_data.items():
                    res_data[int(key)] = {'id': int(val['id']), 'appid': int(val['appid']),
                                          'classid': int(val['classid']), 'name': val['name']}

        # обработка списка ожидающих подтверждения
        if not (confirm_list := resp_data.get('listings_to_confirm')) is None:
            for d_data in confirm_list:
                asset = d_data['asset']
                res_data[int(asset['id'])] = {'id': int(asset['id']), 'appid': int(asset['appid']),
                                              'classid': int(asset['classid']), 'name': asset['name']}

        if get_change:
            return_data = {}
            for key, value in self.sell_list.items():
                if key not in res_data.keys():
                    return_data[key] = value

        self.sell_list = res_data
        return return_data

        # res_data = {}
        #
        # if not (sell_list := resp_data.get('assets')) is None:
        #     for app in sell_list.keys():
        #         app_data = sell_list[app].get('2')
        #         for key, val in app_data.items():
        #             if get_change:
        #                 if int(key) not in self.sell_list.keys():
        #                     res_data[int(key)] = {'id': int(val['id']), 'appid': int(val['appid']), 'classid': int(val['classid']), 'name': val['name']}
        #             else: res_data[int(key)] = {'id': int(val['id']), 'appid': int(val['appid']), 'classid': int(val['classid']), 'name': val['name']}
        #
        # if not (confirm_list := resp_data.get('listings_to_confirm')) is None:
        #     for d_data in confirm_list:
        #         asset = d_data['asset']
        #         if get_change:
        #             if int(asset['id']) not in self.sell_list.keys():
        #                 res_data[int(asset['id'])] = {'id': int(asset['id']), 'appid': int(asset['appid']), 'classid': int(asset['classid']), 'name': asset['name']}
        #         else: res_data[int(asset['id'])] = {'id': int(asset['id']), 'appid': int(asset['appid']), 'classid': int(asset['classid']), 'name': asset['name']}
        #
        # # мб убрать из-за ненадобности
        # # if get_change:
        # #     old_data = self.sell_list
        # #     return_data = {}
        # #     for itemid in old_data.keys():
        # #         if itemid not in res_data.keys():
        # #             return_data[itemid] = old_data[itemid]
        # if not get_change:
        #     self.sell_list = res_data
        #
        # # self.sell_list = res_data
        # return res_data

    def update_buys(self, get_change: bool = False):
        resp_data = self.inv_m.get_selling_items(self.session)
        if (buy_list := resp_data.get('buy_orders')) is None: return

        return_data = None
        res_data = {}
        for el in buy_list:
            res_data[el.get('buy_orderid')] = {'buy_orderid': el['buy_orderid'], 'appid': el['appid'],
                                               'name': el['hash_name'], 'price': el['price'],
                                               'quantity': el['quantity'], 'quantity_remaining': el['quantity_remaining']}
        if get_change:
            old_data = self.buy_list
            return_data = {}
            for orderid in res_data.keys():
                if orderid not in old_data.keys():
                    return_data[orderid] = res_data[orderid]
        self.buy_list = res_data
        return return_data


