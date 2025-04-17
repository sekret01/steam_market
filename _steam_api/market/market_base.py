import json


class BaseMarket:
    """
    Базовый класс для работы с торговой площадки.
    Использовать для наследования
    """
    def __init__(self):
        self._head_path = "_results/input_default_data/headers_market_buy.json"  # без ../
        self.headers: dict[str, str] = {}
        self.set_headers()

    def set_headers(self, headers: dict | None = None) -> None:
        """ обновление загаловка """
        if headers:
            self.headers = headers
            return
        with open(self._head_path, 'r', encoding='utf-8') as file:
            self.headers = json.load(file)

    def _get_session_id(self, cookies: dict) -> str | None:
        """ Получение session_id из cookies """
        if "sessionid" not in cookies.keys(): return None
        return cookies["sessionid"]