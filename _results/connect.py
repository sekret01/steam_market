# from functools import singledispatch
from functools import singledispatchmethod
import requests
import json


class SetsSession(requests.Session):

    def __init__(self):  # , session: requests.Session = None
        super().__init__()


    @singledispatchmethod
    def update_cookies(self, data) -> None:
        """
        The function updates the cookies for the session.
        Data can be submitted in different formats, including in the file.

        Possible data types:

        * str - file name. The file will be searched, its contents will be written in cokies
        * str - raw cookies from the browser. They have the following appearance: 'name1=val1;name2=val2;...'
        * dict - a dictionary of species: {'name1': 'val1', 'name2': 'val2', ...}
        * list[tuple[str,str]] - a list of tuples that look: [('name1', 'val1'),('name2','val2'),...]

        :param data: Any, data for updating cookies
        :return: None
        """
        pass

    @update_cookies.register(list)
    def _(self, data: list[tuple[str,int]]) -> None:
        cookies = {}
        for pare in data:
            cookies[pare[0]] = pare[1]

        try:
            self.cookies.update(cookies)
        except Exception as ex:
            print(ex)
            return

    @update_cookies.register
    def _(self, text: str) -> None:
        try:
            print('try to read file')
            with open(text, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if not isinstance(data, dict):
                    raise TypeError(f"data in file must be dict. Have: {type(data)}")

        except Exception:  # FileNotFoundError:
            split_text = text.split(';')
            data = {}
            for part in split_text:
                s_part = part.split('=')
                if len(s_part) != 2:
                    continue
                data[s_part[0].strip()] = s_part[1].strip()

        # except Exception as ex:
        #     print('upd head 2\n', ex)
        #     return

        try:
            self.cookies.update(data)
        except Exception as ex:
            print(ex)
            return

    @update_cookies.register
    def _(self, data: dict) -> None:
        try:
            self.cookies.update(data)
        except Exception as ex:
            print(ex)
            return


    def save_cookies(self, file_name: str):
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(dict(self.cookies), f)


    @singledispatchmethod
    def update_headers(self, data):
        with open("_results/input_default_data/headers_default.json", 'r', encoding='utf-8') as f:
            headers = json.load(f)
            self.headers.update(headers)


    @update_headers.register
    def _(self, data: dict):
        try:
            self.headers.update(data)
        except Exception as ex:
            print("Error with update headers: \n", ex)
            return

    @update_headers.register
    def _(self, data: str):
        try:
            with open(data, 'r', encoding='utf-8') as f:
                headers = json.load(f)
                if not isinstance(headers, dict):
                    raise TypeError(f"data in file must be dict. Have: {type(data)}")
        except FileNotFoundError as ex:

            res_data = {}
            pares = data.split('\n')

            for pare in pares:
                key, val = pare.split(': ')
                res_data[key] = f'{val}'

            self.headers.update(res_data)

            print("Error with update headers: \n", ex)  # возможна другая обработка
            return
        except Exception as ex:
            print("big error")
            return
        self.headers.update()
