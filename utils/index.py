'''
Desc:
File: /index.py
File Created: Sunday, 23rd July 2023 10:31:51 pm
Author: luxuemin2108@gmail.com
-----
Copyright (c) 2023 Camel Lu
'''
import sqlalchemy
import time
from functools import wraps
import re
from infra.logger.logger import Logger

                 
logger = Logger(file='log/timer.log', logger_format=" [%(asctime)s]  %(levelname)s %(message)s",  show_stream=False)


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


def timeit_with_log(*, is_log=True):
    def timeit_wrapper(func):
        @wraps(func)
        def timeit_wrapper_core(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            total_time = end_time - start_time
            if is_log:
                logger.info(
                    f'Function {func.__name__} {args} {kwargs} Took {total_time:.4f} seconds')
                # print(
                #     f'Function {func.__name__} {args} {kwargs} Took {total_time:.4f} seconds\n')
            return result
        return timeit_wrapper_core
    return timeit_wrapper


def get_symbol_by_code(code, *,  maybe_etf=False):
    """
    根据code规则输出是上证还是深证
    """
    if bool(re.search("^(6|9)\d{5}$", code)):
        symbol = 'SH' + code
    elif bool(re.search("^(3|0|2)\d{5}$", code)):
        symbol = 'SZ' + code
    elif bool(re.search("^(4|8)\d{5}$", code)):
        symbol = 'BJ' + code
    elif bool(re.search("^(11)\d{4}$", code)):  # 沪市可转债
        symbol = 'SH' + code
    elif bool(re.search("^(12)\d{4}$", code)):  # 深市可转债
        symbol = 'SZ' + code
    elif bool(maybe_etf and re.search("^(1)\d{5}$", code)):  # 深市ETF
        symbol = 'SZ' + code
    elif bool(maybe_etf and re.search("^(5)\d{5}$", code)):  # 沪市ETF
        symbol = 'SH' + code
    else:
        print('code', code, '未知')
    return symbol
