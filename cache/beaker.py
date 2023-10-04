from enum import Enum
from datetime import datetime
from beaker.cache import CacheManager
from functools import wraps
from beaker.util import parse_cache_config_options
import pandas as pd

from ..utils.index import timeit

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


def create_cache(*, module, type="file", expire=3600, end: EndMode = None):
    persistence_seconds = expire
    if end:
        now = datetime.now()
        period = pd.Period(value=now, freq=end.value)
        delta = period.end_time - now
        persistence_seconds = delta.seconds

    def _cache_fn(func):
        @timeit
        @wraps(func)
        def wrapper(*args, **kwargs):
            @cache.cache(module, type=type, expire=persistence_seconds)
            def func_dummy(**kwargs):
                print("kwargs", args, kwargs)
                return func(*args, **kwargs)
            return func_dummy(**kwargs)
        return wrapper
    # return cache.cache('temp', type='file', expire=10)
    return _cache_fn
