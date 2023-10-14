'''
Desc:
File: /infra/api/snakball.py
File Created: Sunday, 16th July 2023 11:52:42 pm
Author: luxuemin2108@gmail.com
-----
Copyright (c) 2023 Camel Lu
'''

from datetime import datetime
import os
import dateutil

from infra.cache.beaker import create_cache, EndMode
from infra.utils.index import timeit_with_log
from .base import BaseApier
from ..utils.driver import get_request_header_key


def create_snowball_cache(*args, **kwargs):
    return create_cache(module="snowball", *args, **kwargs)


class ApiSnowBall(BaseApier):
    xue_qiu_cookie = None

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

    def get_portfolio_list(self, *, symbol=None, system=True):
        url = f"{self.base_url}/v5/stock/portfolio/list.json"
        params = {
            'system': system,
            'symbol': symbol
        }
        data = self.get(url, params=params).get("data")
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

    @timeit_with_log()
    def get_kline_info(self, symbol, begin=None, period='day', *, type='before', end=None, rest=dict()):
        params = {
            **rest,
            'symbol': symbol.upper(),
            'period': period,
            'type': 'before' if type == None else type,  # 默认前复权数据
            # JavaScript时间戳 = python时间戳 * 1000
            # 'begin': int(begin_timestamp * 1000),
            'indicator': 'kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance',
            # 'end': int(end_timestamp * 1000),
        }
        """
            begin时间一般是一天开始的时间，end时间一般是一天结束的时间
            所以begin时间戳是一天开始的时间戳，end时间戳是一天结束的时间戳
        """
        if begin:
            begin_timestamp = dateutil.parser.parse(begin).timestamp()
            params['begin'] = int(begin_timestamp * 1000)
        end = end if end else rest.get('end')
        if end:
            end_timestamp = dateutil.parser.parse(end).timestamp()
            params['end'] = int(end_timestamp * 1000)

        url = f"{self.base_url}/v5/stock/chart/kline.json"
        data = self.get(url, params=params).get('data')
        return data

    def get_lastest_kline_info(self, *, symbol: str, date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')):
        rest = {'count': -1}
        res = self.get_kline_info(symbol, begin=date, rest=rest)
        # print("res", res)
        column_keys = res.get('column')
        column_values = res.get('item')[-1]
        info = dict()
        for idx in range(len(column_keys)):
            key = column_keys[idx]
            val = column_values[idx]
            if val != None:
                if key == 'market_capital':
                    val = round(val / 1e8, 2)  # 亿单位
                info[key] = val
        return info

    # @BaseApier.CacheJSON('/data/json/snowball/top_holders')
    @create_snowball_cache(end=EndMode.Month)
    def get_top_holders(self, symbol, *, circula=0, **args):
        params = {
            'symbol':  symbol.upper(),
            'circula': circula,
            **args
        }
        url = f"{self.base_url}/v5/stock/f10/cn/top_holders.json"
        data = self.get(url, params=params).get('data')
        # self.logger.info('data:', data)
        return data
