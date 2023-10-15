'''
Desc:
File: /wglh.py
Project: api
File Created: Sunday, 15th October 2023 9:58:15 pm
Author: luxuemin2108@gmail.com
-----
Copyright (c) 2023 Camel Lu
'''

import time
import json
from infra.cache.beaker import create_cache_based_stack
from .base import BaseApier
from bs4 import BeautifulSoup

class ApiWglh(BaseApier):
    def __init__(self):
        super().__init__()
        referer = 'https://wglh.com/'
        self.referer = referer
        self.base_url = 'https://wglh.com/'
        self.cur_date = time.strftime(
        "%Y-%m-%d", time.localtime(time.time()))
        self.set_client_headers(cookie_env_key='wglh_cookie', referer=self.referer)

    @create_cache_based_stack(is_before_clear=True)
    def get_history_html(self, *, symbol):
        url = f"{self.base_url}stock/history/{symbol}/"
        return self.get_html(url)


    @create_cache_based_stack(is_before_clear=True)
    def get_pe_pb_levels_from_history(self, *, symbol ):
        html = self.get_history_html(symbol = symbol)
        soup = BeautifulSoup(html, "lxml")
        data = soup.find_all('script', type='text/javascript')
        script_content = data[-1].string
        json_string = script_content.split('var positions = ')[1]
        json_string = json_string.split('; ')[0]
        json_string = json_string.replace('\'', '\"')
        value_levels = json.loads(json_string)
        return value_levels
