'''
Desc:
File: /batcher.py
File Created: Saturday, 22nd July 2023 12:17:06 pm
Author: luxuemin2108@gmail.com
-----
Copyright (c) 2023 Camel Lu
'''
from datetime import datetime
import logging
from infra.kline.kline import Kline
import pandas as pd


class KlineBatcher:
    def __init__(self, option: dict) -> None:
        logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                            filename='log/batcher.log',  filemode='a', level=logging.INFO)
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.df_source_data = option.get('source_data')

    def set_params(self, params):
        date = params.get('date') if params.get('date') else self.today
        freq = params.get('freq')

        before_day = params.get('before_day')
        if before_day:
            ts = pd.Timestamp(date).timestamp()
            begin = datetime.fromtimestamp(
                ts - before_day * 24 * 3600).strftime("%Y-%m-%d")
            end = date
        elif freq and not end:
            res = pd.Timestamp(date).to_period(freq=freq)
            begin = res.start_time.strftime('%Y-%m-%d')
            end = res.end_time.strftime('%Y-%m-%d')
        params = {
            **params,
            'date': date,
            'begin': begin,
            'end': end,
        }
        self.params = params

    def calculate(self, *, drawdown_size=100):
        kline_list_map = dict()
        for index, etf_item in self.df_source_data.iterrows():
            code = etf_item.get('code')
            symbol = etf_item.get('market').upper() + code
            name = etf_item.get('name')
            kline = Kline(symbol, name, self.params)
            kline.get_kline_data()
            if len(kline.df_kline) == 0:
                print(f'code:{code}, 没有kline数据')
                kline_list_map[code] = kline.df_kline
                continue
            kline.calculate_ma()
            kline.calculate_mv()
            kline.calculate_drawdown(drawdown_size)
            # kline.calculate_rise()
            kline.df_kline['name'] = name
            kline.df_kline['code'] = code
            kline.df_kline['market'] = etf_item.get('market')
            kline.df_kline['symbol'] = symbol
            # kline.df_kline.to_csv("data/stock_kline.csv", header=True, index=True)
            kline_list_map[code] = kline.df_kline
        self.kline_list_map = kline_list_map
