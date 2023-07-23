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
