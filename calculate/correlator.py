import pandas as pd
from datetime import datetime
from infra.kline.kline import Kline


'''
相关系数绝对值 ：
0.8-1.0 极强相关
0.6-0.8 强相关
0.4-0.6 中等程度相关
0.2-0.4 弱相关
0.0-0.2 极弱相关或无相关
'''


class Correlator():
    def __init__(self, compare_list, end_date, *, size=180):
        self.end_date = end_date
        ts = pd.Timestamp(end_date).timestamp()
        # 取180天的数据比较
        self.begin_date = datetime.fromtimestamp(
            ts - size * 24 * 3600).strftime("%Y-%m-%d")
        benchmark = Kline('SH000300', '沪深300')
        benchmark.set_params({
            'period': 'day',
            'begin': self.begin_date,
            'end': end_date,
        })
        benchmark.set_kline_data(is_slice=True)
        self.benchmark_len = len(benchmark.df_kline)
        self.compare_list = compare_list

    def prepare_compare(self, compares, exist_compares=[]):
        if not isinstance(compares, pd.DataFrame):
            compares = pd.DataFrame(compares)
        compare_list = []
        exist_symbols = []
        begin_date = self.begin_date
        end_date = self.end_date
        for item in exist_compares:
            symbol = item.get('symbol')
            exist_symbols.append(symbol)
            name = item.get('name')
            compare = Kline(symbol, name)
            compare.set_params({
                'period': 'day',
                'begin': self.begin_date,
                'end': end_date,
            })
            compare_list.append(compare)
        for index, item in compares.iterrows():
            item_symbol = item.get('symbol')
            if item_symbol == None:
                item_symbol = item.get('market').upper() + item.get('code')
            if item_symbol in exist_symbols:
                continue
            item_name = item.get('name')
            compare = Kline(item_symbol, item_name)
            compare.set_params({
                'period': 'day',
                'begin': self.begin_date,
                'end': end_date,
            })
            compare.set_kline_data(is_slice=True)
            compare_list.append(compare)
        self.compare_list = compare_list
        return self

    def correlate(self, output=False):
        df_compare = pd.DataFrame()
        un_compare_data = []
        kline_compare_list = []
        for item in self.compare_list:
            compare = Kline(item.get('symbol'), item.get('name'))
            compare.set_params({
                'period': 'day',
                'begin': self.begin_date,
                'end':  self.end_date,
            })
            compare.set_kline_data(is_slice=True)
            kline_compare_list.append(compare)
        for item in kline_compare_list:
            # 长度不一致,不能比较
            begin_date = pd.to_datetime(self.begin_date).date()
            end_date = pd.to_datetime(self.end_date).date()
            try:
                compare_data = item.df_kline.loc[begin_date:end_date]
            except:
                compare_data = item.df_kline.loc[self.begin_date:self.end_date]
            if self.benchmark_len != len(compare_data):
                un_compare_data.append({
                    '证券名称': item.name,
                    '证券代码': item.symbol
                })
                continue
            # item.ks_test()
            column_name = item.name + '(' + item.symbol + ')'
            df_compare[column_name] = compare_data['close'].values
        res = df_compare.corr()
        res_by_spearman = df_compare.corr(method='spearman')
        res_mean = ((res_by_spearman + res)/2).round(3)  # 两种比较取均值
        # res_mean.to_csv('data/rise.csv')
        self.res_compare = res_mean
        if output:
            # print('不参加评比指数有{}名:'.format(len(un_compare_data)))
            if len(un_compare_data) > 0:
                df_uncompare = pd.DataFrame(un_compare_data).set_index("证券名称")
                # print(df_uncompare.to_markdown())
            if len(self.res_compare) <= 1:
                return res_mean
            # 返回第一个与第二个相似值
            return (res.iat[0, 1] + res_by_spearman.iat[0, 1])/2

    def filter_near_similarity(self, threshold=0.6):
        # df = pd.read_csv('data/rise.csv').set_index('Unnamed: 0')
        # print(df)
        df = self.res_compare
        # cur = '商品ETF'
        excludes = []
        for index, item in df.iterrows():
            if index not in excludes:
                for key in item.keys():
                    if key != index and item.get(key) > threshold and key not in excludes:
                        excludes.append(key)
                        df.drop([key], inplace=True)
                        df.drop(columns=[key], inplace=True)
        # print(excludes)
        return df


if __name__ == '__main__':
    correlator = Correlator([
        {
            'name': '沪深300',
            'symbol': 'SH000300'
        },
        {
            'name': '中证500',
            'symbol': 'SH000905'
        },
        {
            'name': '中证1000',
            'symbol': 'SH000852'
        }
    ], '2023-07-21')
    correlator.correlate()
    print(correlator.res_compare)

    df_similarity = correlator.filter_near_similarity(0.9)
    print(df_similarity)
