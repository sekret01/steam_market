from typing import Literal, Union


class UrlBuilder:
    """
    Объект для настройки url
    Данные функции (кроме add_root() и add_parameters) написаны 
    для SteapAIP, работа с другими сервисами не предусмотрена
    """
    
    def __init__(self, url_base: str | None = None, injson: bool = True):
        if url_base is None:
            self.url: str = ""
        else:
            self.fit(url_base, injson)

    def fit(self, url_base: str, injson: bool):
        self.url = url_base + '?'
        if injson:
            self.url += "norender=1"

    def get_url(self) -> str:
        return self.url


    def add_root(self, root: Union[str, int]):
        self.url = self.url[:-1]
        self.url += f"/{root}?"

    def add_parameters(self, params: dict):
        for key, val in params.items():
            self.url += f"&{key}={val}"

    def add_app_id(self, app_id: int):
        self.url += f"&appid={app_id}"

    def add_count(self, count: int) -> None:
        self.url += f"&count={count}"

    def add_sort(self, sort_by: Literal['price', 'quantity']):
        self.url += f"&sort_column={sort_by}"

    def add_sort_dir(self, s_dir: Literal['asc', 'desc']):
        self.url += f"&sort_dir={s_dir}"

    def add_country(self, country: str):
        """ short country (Ex: `RU`) """
        self.url += f"&country={country}"

    def add_language(self, language: str):
        """ Ex: `russian` """
        self.url += f"&language={language}"

    def add_currency(self, currency_code: int):
        self.url += f"&currency={currency_code}"
