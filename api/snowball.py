'''
Desc:
File: /infra/api/snakball.py
File Created: Sunday, 16th July 2023 11:52:42 pm
Author: luxuemin2108@gmail.com
-----
Copyright (c) 2023 Camel Lu
'''

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

    def get(self, url, **kwargs):
        response = self.session.get(url, headers=self.headers, **kwargs)
        try:
            if response.status_code == 200:
                return response.json().get('data')
        except:
            raise ('请求异常')

    def get_portfolio_list(self, *, system=True):
        url = f"{self.base_url}/v5/stock/portfolio/list.json?system={system}"
        data = self.get(url)
        return data

    def get_portfolio_stocks(self, pid, *, category=1, size=1000):
        params = {
            'pid': pid,
            'category': category,
            'size': size
        }
        url = f"{self.base_url}/v5/stock/portfolio/stock/list.json"
        data = self.get(url, params=params)
        return data

    def get_kline_info(self, symbol, begin, period, *, type='before', rest=dict()):
        begin_timestamp = dateutil.parser.parse(begin).timestamp()
        end = rest.get('end')
        if end:
            end_timestamp = dateutil.parser.parse(end).timestamp()
            rest['end'] = int(end_timestamp * 1000)
        params = {
            **rest,
            'symbol': symbol.upper(),
            'period': period,
            'type': 'before' if type == None else type,  # 默认前复权数据
            # JavaScript时间戳 = python时间戳 * 1000
            'begin': int(begin_timestamp * 1000),
            'indicator': 'kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance',
            # 'end': int(end_timestamp * 1000),
        }
        url = f"{self.base_url}/v5/stock/chart/kline.json"
        data = self.get(url, params=params)
        return data
