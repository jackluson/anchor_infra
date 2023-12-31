import os
import inspect
from enum import Enum
from datetime import datetime
from beaker.cache import CacheManager
from functools import wraps
from beaker.util import parse_cache_config_options
import pandas as pd

from infra.utils.index import timeit_with_log
from infra.logger.logger import Logger

cache_opts = {
    'cache.type': 'file',
    'cache.data_dir': './tmp/cache/data',
    'cache.lock_dir': './tmp/cache/lock'
}


class EndMode(Enum):
    Day = 'D'
    Month = 'M'
    Quarter = 'Q'


cache = CacheManager(**parse_cache_config_options(cache_opts))


def create_cache(*, module, type="file", expire=3600, end: EndMode = None, use_in_class=True, is_before_clear=False):
    persistence_seconds = expire
    if end:
        now = datetime.now()
        period = pd.Period(value=now, freq=end.value)
        delta = period.end_time - now
        persistence_seconds = round(delta.total_seconds())
    def _cache_fn(func):
        @timeit_with_log(is_log=True)
        @wraps(func)
        def wrapper(*args, **kwargs):
            @cache.cache(module, type=type, expire=persistence_seconds)
            def func_dummy(*_args, **_kwargs):
                return func(*args, **kwargs)
            # 第一个参数是self，排除
            temp_args = args[1:] if use_in_class else args
            if is_before_clear:
                cache.invalidate(func_dummy, module, func.__name__, *temp_args, *kwargs.items(), type="file")
            return func_dummy(func.__name__, *temp_args, *kwargs.items())
        return wrapper
    # return cache.cache('temp', type='file', expire=10)
    return _cache_fn

def create_cache_based_stack(*, expire=3600, end=EndMode.Day, is_before_clear=False):
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    filename = os.path.basename(module.__file__)
    return create_cache(module=filename, expire=expire, end=end, is_before_clear=is_before_clear)
