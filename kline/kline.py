'''
Desc:
File: /kline.py
File Created: Wednesday, 19th July 2023 11:15:45 pm
Author: luxuemin2108@gmail.com
-----
Copyright (c) 2023 Camel Lu
'''

import os
import pandas as pd
from infra.api.snowball import ApiSnowBall
import logging
from datetime import datetime
pd.options.mode.chained_assignment = None

save_begin_date = '2016-01-01'
save_end_date = '2023-06-30'

save_archive_dir = "./data/csv/period/"
archive_dir = "./data/csv/"


class Kline:
    def __init__(self, symbol, name, params):
        self.date = None
        self.freq = 'D'
        self.api = ApiSnowBall()
        self.symbol = symbol
        self.name = name
        logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                            filename='log/stock_kline_info.log',  filemode='a', level=logging.INFO)
        self.set_params(params)

    def set_params(self, params):
        params = {
            'period': 'day',
            **params,
        }
        self.params = params

    def fetch_kline_data(self):
        begin = self.params.get('begin')
        type = self.params.get('type')
        period = self.params.get('period')
        response = self.api.get_kline_info(
            self.symbol, begin, period, type=type, rest=self.params)
        columns = response["column"]
        items = response["item"]
        pd.Series(items)
        df = pd.DataFrame(items, columns=columns)
        if df.empty:
            line = f'该{self.name}--{self.symbol}没有查到数据--{begin}--{self.params}'
            logging.info(line)
            return df
        else:
            df = df[['timestamp', 'open', 'close', 'low', 'high', 'chg',
                     'percent', 'volume', 'amount', 'market_capital']]
            df['timestamp'] = df['timestamp'] / 1000
            df['timestamp'] = pd.to_datetime(
                df['timestamp'], unit='s', utc=True)
            df = df.set_index('timestamp').tz_convert('Asia/Shanghai')
            df['date'] = df.index.date.astype(str)
            df = df.set_index('date')
            return df

    def set_kline_data(self, *, is_slice=False):
        begin = self.params.get('begin')
        end = self.params.get('end')
        type = self.params.get('type')
        count = self.params.get('count')
        period = self.params.get('period')
        is_in_date = False
        in_date_file = f"{save_archive_dir}{self.symbol}_{save_begin_date}_{save_end_date}_{period}.csv"
        if end:
            filename = f"{archive_dir}{self.symbol}_{begin}_{end}_{period}.csv"
            is_in_date = pd.Timestamp(end).timestamp() <= pd.Timestamp(save_end_date).timestamp(
            ) and pd.Timestamp(begin).timestamp() >= pd.Timestamp(save_begin_date).timestamp()
        elif count:
            filename = f"{archive_dir}{self.symbol}_{begin}_{type}_{str(count)}_{period}.csv"
        is_exist_file = os.path.exists(filename)
        if is_exist_file:
            df_stock_kline_info = pd.read_csv(filename, index_col=[
                                              'date'], parse_dates=['date'])
        elif is_in_date and os.path.exists(in_date_file):
            df_stock_kline_info = pd.read_csv(
                in_date_file, index_col=['date'], parse_dates=['date'])
            if is_slice:
                df_stock_kline_info = df_stock_kline_info.loc[begin:end]
        else:
            df_stock_kline_info = self.fetch_kline_data()
            df_stock_kline_info.to_csv(filename)
        self.df_kline = df_stock_kline_info

    def calculate_period_percent(self, before_day_count=None, is_format_str=False):
        if (self.df_kline.empty):
            print(self.symbol, 'K线数据为空:', self.df_kline)
            return None
        start_net = self.df_kline.loc[self.df_kline.index[0]]['close']
        start_chg = self.df_kline.loc[self.df_kline.index[0]]['chg']
        if before_day_count and len(self.df_kline) > before_day_count:
            start_net = self.df_kline.iloc[-(before_day_count)]['close']
            start_chg = self.df_kline.iloc[-(before_day_count)]['chg']
        start_net = start_net - start_chg
        last_net = self.df_kline.loc[self.df_kline.index[-1]]['close']
        percent = round((last_net - start_net)/start_net*100, 2)
        if percent and is_format_str:
            percent = str(percent) + '%'
        return percent

    def get_past_mean(self, dimension, before_days=5, round_num=3):
        if self.df_kline.empty:
            return None
        return self.df_kline[dimension].tail(before_days).mean().round(round_num)

    def calculate_ma(self):
        self.df_kline['ma5'] = self.df_kline['close'].rolling(
            5).mean().round(2)
        self.df_kline['ma10'] = self.df_kline['close'].rolling(
            10).mean().round(2)
        self.df_kline['ma20'] = self.df_kline['close'].rolling(
            20).mean().round(2)
        self.df_kline['ma30'] = self.df_kline['close'].rolling(
            30).mean().round(2)
        self.df_kline['ma60'] = self.df_kline['close'].rolling(
            60).mean().round(2)
        self.df_kline['ma120'] = self.df_kline['close'].rolling(
            120).mean().round(2)

    def calculate_mv(self):
        self.df_kline['mv4'] = self.df_kline['volume'].rolling(
            4).mean().round(2)
        self.df_kline['mv8'] = self.df_kline['volume'].rolling(
            8).mean().round(2)
        self.df_kline['mv20'] = self.df_kline['volume'].rolling(
            20).mean().round(2)
        self.df_kline['mv30'] = self.df_kline['volume'].rolling(
            30).mean().round(2)

        self.df_kline['max_mv4'] = self.df_kline['volume'].rolling(
            4, min_periods=1).max()
        self.df_kline['max_percent4'] = self.df_kline['percent'].rolling(
            4, min_periods=1).max()

    def calculate_drawdown(self, size=100):
        day_cnt = size
        max_close_key = 'max_close_'+str(day_cnt)
        min_close_key = 'min_close_'+str(day_cnt)
        dd_key = 'dd_'+str(day_cnt)
        max_dd_key = 'max_dd_'+str(day_cnt)
        # 计算每一天的最近最大回撤幅度, min_periods一定要设置为1, 否则会出现max_dd_key出现问题
        self.df_kline[min_close_key] = self.df_kline['close'].rolling(
            day_cnt, min_periods=1).min()
        # self.df_kline[max_close_key] = self.df_kline['close'].expanding(min_periods=day_cnt).max()
        self.df_kline[max_close_key] = self.df_kline['close'].rolling(
            day_cnt, min_periods=1).max()
        self.df_kline[dd_key] = (
            (self.df_kline['close'] - self.df_kline[max_close_key]) / self.df_kline[max_close_key]).round(4)
        self.df_kline[max_dd_key] = self.df_kline[dd_key].rolling(
            day_cnt, min_periods=1).min().round(4)

    def calculate_rise(self):
        # 过去20天的最低价
        self.df_kline['min_price_20'] = self.df_kline['close'].rolling(
            20, min_periods=1).min().round(4)

        # 计算每一天的涨幅相对低点的涨幅
        self.df_kline['increase_20'] = (
            (self.df_kline['close'] - self.df_kline['min_price_20']) / self.df_kline['min_price_20']).round(4)
        self.df_kline['min_price_10'] = self.df_kline['close'].rolling(
            10, min_periods=1).min().round(4)

        # 计算每一天的涨幅相对低点的涨幅
        self.df_kline['increase_10'] = (
            (self.df_kline['close'] - self.df_kline['min_price_10']) / self.df_kline['min_price_10']).round(4)


if __name__ == '__main__':
    benchmark = Kline('SH000300', '沪深300', {
        'period': 'day',
        'begin': '2023-01-01',
        'end': '2023-06-01',
    })

    benchmark.set_kline_data(is_slice=True)
