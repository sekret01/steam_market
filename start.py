"""

Запустить перед началом работы если последние cookies
уже не действительны.
Вставить в переменную _cookies строку с данными, взятую из Request Headers

"""

from _results import SetsSession
import datetime


if __name__ == "__main__":
    cookies_path = "_results/input_default_data/cookies_for_steam.json"
    headers_path = "_results/input_default_data/headers_default.json"

    _cookies = ""

    SESSION = SetsSession()
    SESSION.update_headers(headers_path)
    SESSION.update_cookies(_cookies)
    SESSION.save_cookies("saved_data/cookies.json")
    print(f"[{datetime.datetime.now().strftime("%H:%M:%S")}] перезапись данных cookies")
