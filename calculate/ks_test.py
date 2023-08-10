'''
Desc:
File: /ks_test.py
File Created: Sunday, 23rd July 2023 5:24:03 pm
Author: luxuemin2108@gmail.com
-----
Copyright (c) 2023 Camel Lu
'''
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from infra.kline.kline import Kline
from datetime import datetime


class KSTestor(Kline):
    def __init__(self, symbol, name, params):
        super().__init__(symbol, name, params)
        self.set_kline_data(is_slice=True)

    def test(self, show=False):
        u = self.df_kline['close'].mean()  # 计算均值
        std = self.df_kline['close'].std()  # 计算标准差
        res = stats.kstest(self.df_kline['close'], 'norm', (u, std))
        # print('res', u, std, res[1])
        self.pass_ks_test = res[1] > 0.05

        if show:
            fig = plt.figure(figsize=(10, 6))
            ax1 = fig.add_subplot(2, 1, 1)  # 创建子图1
            ax1.scatter(self.df_kline.index, self.df_kline['close'].values)
            plt.grid()
            ax2 = fig.add_subplot(2, 1, 2)  # 创建子图2
            self.df_kline['close'].hist(bins=30, alpha=0.5, ax=ax2)
            self.df_kline['close'].plot(kind='kde', secondary_y=True, ax=ax2)
            plt.grid()
            plt.show()


if __name__ == '__main__':
    ksTestor = KSTestor('SH000300', '沪深300', {
        'period': 'day',
        'begin': '2023-01-01',
        'end': '2023-06-01',
    })
    ksTestor.test(show=True)
