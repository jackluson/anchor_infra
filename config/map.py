'''
Desc:
File: /map.py
File Created: Sunday, 6th August 2023 7:52:03 pm
Author: luxuemin2108@gmail.com
-----
Copyright (c) 2023 Camel Lu
'''


rename_cb_map = {
    'id': 'id',
    'cb_id': 'id',
    'cb_code': '可转债代码',
    'cb_name': '可转债名称',
    'stock_code': '股票代码',
    'stock_name': '股票名称',
    'industry': '行业',
    'price': '转债价格',
    'stock_stdevry': '正股波动率',
    'premium_rate': '转股溢价率',
    'cb_to_pb': '转股价格/每股净资产',
    'date_remain_distance': '距离到期时间',
    'date_return_distance': '距离回售时间',
    'rate_expire': '到期收益率',
    'rate_expire_aftertax': '税后到期收益率',
    'remain_to_cap': '转债剩余/市值比例',
    'is_repair_flag': '是否满足下修条件',
    'repair_flag_remark': '下修备注',
    'pre_ransom_remark': '预满足强赎备注',
    'is_ransom_flag': '是否满足强赎条件',
    'ransom_flag_remark': '强赎备注',

    'remain_amount': '剩余规模',
    'trade_amount': '成交额',
    'turnover_rate': '换手率',
    'market_cap': '股票市值',

    'last_price': '上期转债价格',
    'last_cb_percent': '较上期涨跌幅',
    'cb_percent': '转债涨跌幅',
    'stock_price': '股价',
    'stock_percent': '股价涨跌幅',
    'last_stock_price': '上期股价',
    'last_stock_percent': '较上期股价涨跌幅',
    'arbitrage_percent': '日内套利',
    'convert_stock_price': '转股价格',
    'pb': '市净率',
    'market': '市场',

    'remain_price': '剩余本息',
    'remain_price_tax': '税后剩余本息',

    'is_unlist': '未发行',
    'last_is_unlist': '上期未发行',
    'issue_date': '发行日期',
    'date_convert_distance': '距离转股时间',

    'rate_return': '回售收益率',

    'old_style': '老式双底',
    'new_style': '新式双底',
    'rating': '债券评级',
    'weight': '多因子得分',
}

ingore_columns = [
    rename_cb_map['id'],
    rename_cb_map['cb_id'],
    rename_cb_map['cb_code'],
    rename_cb_map['cb_name'],
    rename_cb_map['stock_code'],
    rename_cb_map['stock_name'],
    rename_cb_map['industry'],
    rename_cb_map['price'],
    rename_cb_map['market'],
    rename_cb_map['stock_price'],
    rename_cb_map['last_stock_price'],
    rename_cb_map['last_stock_percent'],
    rename_cb_map['arbitrage_percent'],
    rename_cb_map['weight'],
]
