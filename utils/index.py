'''
Desc:
File: /index.py
File Created: Sunday, 23rd July 2023 10:31:51 pm
Author: luxuemin2108@gmail.com
-----
Copyright (c) 2023 Camel Lu
'''
import time
from functools import wraps
import re


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(
            f'Function {func.__name__} {kwargs} Took {total_time:.4f} seconds\n')
        return result
    return timeit_wrapper


def get_symbol_by_code(stock_code):
    """
    根据code规则输出是上证还是深证
    """
    if bool(re.search("^(6|9)\d{5}$", stock_code)):
        symbol = 'SH' + stock_code
    elif bool(re.search("^(3|0|2)\d{5}$", stock_code)):
        symbol = 'SZ' + stock_code
    elif bool(re.search("^(4|8)\d{5}$", stock_code)):
        symbol = 'BJ' + stock_code
    else:
        print('code', stock_code, '未知')
    return symbol
