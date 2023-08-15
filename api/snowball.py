'''
Desc:
File: /infra/api/snakball.py
File Created: Sunday, 16th July 2023 11:52:42 pm
Author: luxuemin2108@gmail.com
-----
Copyright (c) 2023 Camel Lu
'''

import json
import os
import dateutil

from .base import BaseApier
from ..utils.driver import get_request_header_key


class ApiSnowBall(BaseApier):
    def __init__(self, need_login=False):
        origin = 'https://xueqiu.com'
        host = 'xueqiu.com'
        self.base_url = "https://stock.xueqiu.com"
        super().__init__()
        self.xue_qiu_cookie = os.getenv('xue_qiu_cookie')
        if need_login and not self.xue_qiu_cookie:
            raise Exception('need login')
        elif not self.xue_qiu_cookie:
            xue_qiu_cookie = get_request_header_key(
                origin, host, 'Cookie')
            self.xue_qiu_cookie = xue_qiu_cookie
        self.set_client_headers()

    def get_portfolio_list(self, *, system=True):
        url = f"{self.base_url}/v5/stock/portfolio/list.json?system={system}"
        data = self.get(url).get("data")
        return data

    def get_portfolio_stocks(self, pid, *, category=1, size=1000):
        url = f"{self.base_url}/v5/stock/portfolio/stock/list.json?pid={pid}&category={category}&size={size}"
        data = self.get(url).get("data")
        return data

    def add_portfolio(self, symbols):
        url = f"{self.base_url}/v5/stock/portfolio/stock/add.json"
        payload = {
            "symbols": symbols,
        }
        res = self.post(url, data=payload)
        if res.get('data') != True:
            print('add_portfolio failed pls check')
        return res

    def cancel_portfolio(self, symbols):
        url = f"{self.base_url}/v5/stock/portfolio/stock/cancel.json"
        payload = {
            "symbols": symbols,
        }
        res = self.post(url, data=payload)
        if res.get('data') != True:
            print('add_portfolio failed pls check')
        return res

    def modify_portfolio(self, symbols, pnames, *, category=1):
        url = f"{self.base_url}/v5/stock/portfolio/stock/modify_portfolio.json"
        payload = {
            "symbols": symbols,
            "pnames": pnames,
            "category": category,
        }
        res = self.post(url, data=payload)
        if res.get('data') != True:
            print('modify_portfolio failed pls check')
        return res
