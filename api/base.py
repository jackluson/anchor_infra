'''
Desc:
File: /base.py
File Created: Sunday, 9th July 2023 10:10:31 am
Author: luxuemin2108@gmail.com
-----
Copyright (c) 2023 Camel Lu
'''
import os
from dotenv import load_dotenv


class BaseApier:
    headers = dict()

    def __init__(self):
        load_dotenv()

    def set_client_headers(self, *,  cookie_env_key="xue_qiu_cookie", referer="https://xueqiu.com", origin=None):
        cookie = self.__dict__.get(cookie_env_key)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36',
            'Origin': origin if origin else referer,
            'Referer': referer if referer else self.referer,
            'Cookie': cookie
        }
        self.headers = headers
        return headers
