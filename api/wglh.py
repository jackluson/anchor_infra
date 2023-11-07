'''
Desc:
File: /wglh.py
Project: api
File Created: Sunday, 15th October 2023 9:58:15 pm
Author: luxuemin2108@gmail.com
-----
Copyright (c) 2023 Camel Lu
'''

import sqlalchemy
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

    def get_history_html(self, *, symbol):
        url = f"{self.base_url}stock/history/{symbol}/"
        return self.get_html(url)


    def get_pe_pb_levels_from_history(self, *, symbol ):
        html = self.get_history_html(symbol = symbol)
        if html == None:
            return None
        soup = BeautifulSoup(html, "lxml")
        fmt_items = soup.find_all('div', {'class': "fdm"})[0].find_all('div', {'class': "item"})
        pb_value = None
        pe_value = None
        pe_kf_value = None
        for items in fmt_items:
            label =  items.find_all('span', {'class': "name"})[0].get_text()
            value =  items.find_all('span', {'class': "value"})[0]
            if label == '市净率PB：':
                pb_value = value.get_text()
            elif label == 'PE/扣非PE：':
                item_values = value.get_text().split('/')
                pe_value = item_values[0]
                pe_kf_value = item_values[1]
            if pb_value and pe_value and pe_kf_value:
                break
            
        data = soup.find_all('script', type='text/javascript')
        script_content = data[-1].string
        json_string = script_content.split('var positions = ')[1]
        json_string = json_string.split('; ')[0]
        json_string = json_string.replace('\'', '\"')
        value_levels = json.loads(json_string)
        return {
            'pb': {
                **value_levels['pb'],
                'value': pb_value,
            },
            'pe': {
                **value_levels['pe'],
                'value': pe_value,
            },
            'pe_koufei': {
                 **value_levels['pe_koufei'],
                'value': pe_kf_value,
            },
        }
