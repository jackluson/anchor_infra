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
from infra.utils.index import timeit
import pandas as pd
from infra.utils.enum import Freq, Scene


class KlineBatcher:
    scene = Scene.MOMENTUM
    periods_list = []
    today = datetime.now().strftime("%Y-%m-%d")

    def __init__(self, option: dict) -> None:
        logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                            filename='log/batcher.log',  filemode='a', level=logging.INFO)
        self.df_source_data = option.get('source_data')
        if option.get('scene'):
            self.scene = option.get('scene')

    def set_params(self, params):
        freq = params.get('freq')
        end = params.get('end')
        begin = params.get('begin')
        before_day = params.get('before_day')
        if before_day and not begin:
            ts = pd.Timestamp(end).timestamp()
            begin = datetime.fromtimestamp(
                ts - before_day * 24 * 3600).strftime("%Y-%m-%d")
        elif freq and not end:
            date = params.get('date') if params.get('date') else self.today
            res = pd.Timestamp(date).to_period(freq=freq.value)
            begin = res.start_time.strftime('%Y-%m-%d')
            end = res.end_time.strftime('%Y-%m-%d')
        params = {
            **params,
            'begin': begin,
            'end': end,
        }
        self.params = params

    def set_periods_list(self):

        target_date = self.params.get('end')
        period_week_dict = pd.Timestamp(
            target_date).to_period(freq=Freq.WEEK.value)

        period_month_dict = pd.Timestamp(
            target_date).to_period(freq=Freq.MONTH.value)

        period_year_dict = pd.Timestamp(
            target_date).to_period(freq=Freq.YEAD.value)

        begin_week = period_week_dict.start_time.strftime('%Y-%m-%d')
        end_week = period_week_dict.end_time.strftime('%Y-%m-%d')

        begin_month = period_month_dict.start_time.strftime('%Y-%m-%d')
        end_month = period_month_dict.end_time.strftime('%Y-%m-%d')

        begin_year = period_year_dict.start_time.strftime('%Y-%m-%d')
        end_year = period_year_dict.end_time.strftime('%Y-%m-%d')

        begin_recent_days_10 = pd.Timestamp(
            target_date) - pd.DateOffset(days=10)
        begin_recent_days_20 = pd.Timestamp(
            target_date) - pd.DateOffset(days=20)
        begin_recent_days_30 = pd.Timestamp(
            target_date) - pd.DateOffset(days=30)
        begin_recent_days_60 = pd.Timestamp(
            target_date) - pd.DateOffset(days=60)
        begin_recent_month_3 = pd.Timestamp(
            target_date) - pd.DateOffset(months=3)

        periods_list = [
            {
                'key': 'week_increase',
                'name': '周涨幅',
                'begin': begin_week,
                'end': end_week,
            },
            {
                'key': 'month_increase',
                'name': '月涨幅',
                'begin': begin_month,
                'end': end_month,
            },
            {
                'key': 'year_increase',
                'name': '年涨幅',
                'begin': begin_year,
                'end': end_year,
            },
            {
                'key': 'recent_day_10_increase',
                'name': '近10日涨幅',
                'begin': begin_recent_days_10.strftime('%Y-%m-%d'),
                'end': target_date,
            },
            {
                'key': 'recent_day_20_increase',
                'name': '近20日涨幅',
                'begin': begin_recent_days_20.strftime('%Y-%m-%d'),
                'end': target_date,
            },
            {
                'key': 'recent_day_30_increase',
                'name': '近30日涨幅',
                'begin': begin_recent_days_30.strftime('%Y-%m-%d'),
                'end': target_date,
            },
            {
                'key': 'recent_day_60_increase',
                'name': '近30日涨幅',
                'begin': begin_recent_days_60.strftime('%Y-%m-%d'),
                'end': target_date,
            },
            {
                'key': 'recent_month_3_increase',
                'name': '近3个月涨幅',
                'begin': begin_recent_month_3.strftime('%Y-%m-%d'),
                'end': target_date,
            },
        ]
        self.periods_list = periods_list

    @timeit
    def calculate(self, *, drawdown_size=100):
        kline_list_map = dict()
        if self.scene == Scene.STATS:
            self.set_periods_list()
        for index, source_item in self.df_source_data.iterrows():
            if index % 50 == 0:
                print('progress:', index)
            code = source_item.get('code')
            symbol = source_item.get('market').upper() + code
            name = source_item.get('name')
            kline = Kline(symbol, name, {
                # 'load_local': False
                # 'save_local': False
            })
            kline.set_params(self.params)
            kline.set_kline_data()
            kline.df_kline['name'] = name
            kline.df_kline['code'] = code
            kline.df_kline['market'] = source_item.get('market')
            kline.df_kline['symbol'] = symbol
            if len(kline.df_kline) == 0:
                print(f'code:{code}, 没有kline数据')
                kline_list_map[code] = kline.df_kline
                continue
            if self.scene == Scene.MOMENTUM:
                kline.calculate_mv()
                kline.calculate_ma()
                kline.calculate_drawdown(drawdown_size)
            if self.scene == Scene.STATS:
                kline.set_increase(self.periods_list)
            if self.scene == Scene.TREND:
                kline.calculate_ma()
            # kline.df_kline.to_csv("data/stock_kline.csv", header=True, index=True)
            kline_list_map[code] = kline.df_kline
        self.kline_list_map = kline_list_map
