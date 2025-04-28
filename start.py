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

    _cookies = "ActListPageSize=100; browserid=3219597558517195650; cookieSettings=%7B%22version%22%3A1%2C%22preference_state%22%3A1%2C%22content_customization%22%3Anull%2C%22valve_analytics%22%3Anull%2C%22third_party_analytics%22%3Anull%2C%22third_party_content%22%3Anull%2C%22utm_enabled%22%3Atrue%7D; timezoneOffset=10800,0; rgDiscussionPrefs=%7B%22cTopicRepliesPerPage%22%3A30%7D; recentlyVisitedAppHubs=706990%2C3419430; strInventoryLastContext=440_2; sessionid=7b0f08e761bcae121b0ec8d6; steamDidLoginRefresh=1745736036; steamCountry=RU%7C91ae04cba9273fd7c5e999124b23fa66; steamLoginSecure=76561199143424949%7C%7CeyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MDAwNl8yNjBDRDExN19DOTk4RiIsICJzdWIiOiAiNzY1NjExOTkxNDM0MjQ5NDkiLCAiYXVkIjogWyAid2ViOmNvbW11bml0eSIgXSwgImV4cCI6IDE3NDU4MjI4NjcsICJuYmYiOiAxNzM3MDk2MDM2LCAiaWF0IjogMTc0NTczNjAzNiwgImp0aSI6ICIwMDE2XzI2MzFCQzIyX0JFRjU4IiwgIm9hdCI6IDE3NDMzNzEzNDAsICJydF9leHAiOiAxNzYxMzQ5MjA0LCAicGVyIjogMCwgImlwX3N1YmplY3QiOiAiNS4xOC4xNTAuMTc2IiwgImlwX2NvbmZpcm1lciI6ICIxNzYuNTkuOS4xNjIiIH0.3r5dqANFU24EJqCxb8oEdI_IsPXGQOCPZ5fdG8K8wftxu-dGy7ibbMAD7KiKN7yYaKAUi5VkaR4kI2eHzQCpAA; webTradeEligibility=%7B%22allowed%22%3A1%2C%22allowed_at_time%22%3A0%2C%22steamguard_required_days%22%3A15%2C%22new_device_cooldown_days%22%3A0%2C%22time_checked%22%3A1745736037%7D"

    SESSION = SetsSession()
    SESSION.update_headers(headers_path)
    SESSION.update_cookies(_cookies)
    SESSION.save_cookies("saved_data/cookies.json")
    print(f"[{datetime.datetime.now().strftime("%H:%M:%S")}] перезапись данных cookies")
