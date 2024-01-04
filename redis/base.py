
from datetime import datetime, timedelta
import json
import pytz
import redis
from infra.config.env import env_redis_db, env_redis_host, env_redis_password, env_redis_port


import decimal
class DecimalEncoder(json.JSONEncoder): 
    def default(self, o): 
        if isinstance(o, decimal.Decimal): return str(o) 
        return super().default(o)

class BaseRedis(object):
    client:redis.Redis = None
    def __init__(self):
        self.client = redis.StrictRedis(host=env_redis_host, port=env_redis_port, db=env_redis_db, password=env_redis_password, decode_responses=True)

    def set(self, *arg, **kwargs):
        return self.client.set(*arg, **kwargs)
    def get(self, *arg, **kwargs):
        return self.client.get(*arg, **kwargs)

    def hset(self, *arg, **kwargs):
        expire = kwargs.pop('expire', None)
        mapping = kwargs.pop('mapping', None)
        self.client.hset(*arg, mapping=mapping, **kwargs)
        if expire:
            self.client.expire(arg[0], expire)
    def hget(self, *arg, **kwargs):
        return self.client.hget(*arg, **kwargs)
    def hgetall(self, *arg, **kwargs):
        return self.client.hgetall(*arg, **kwargs)
    
    def set_with_dumps(self, key, value, expire=2 * 60 * 60):
        encoded_data = json.dumps(value, cls=DecimalEncoder)
        return self.set(key, encoded_data, expire)

    def get_with_loads(self, key):
        res = self.get(key)
        if res:
        # Retrieve the data from Redis and decode it using json.loads
          decoded_data = json.loads(res)
          return decoded_data

    def get_expire_seconds_based_quote(self):
        tz=pytz.timezone('Asia/Shanghai')
        now = datetime.now(tz=tz)
        # start_of_day = datetime(now.year, now.month, now.day, 0, 0, 0)
        #如果是15点之前，那么过期时间就是今天15点，否则就是明天15点
        timedelta_day = 1
        weekday = now.weekday()
        if now.hour < 15 and 0 <= weekday < 5:
            expire_by = datetime(now.year, now.month, now.day, 15, 0, 0, tzinfo=tz)
        else:
            if weekday == 4:
                timedelta_day = 3
            elif weekday == 5:
                timedelta_day = 2
            expire_by = datetime(now.year, now.month, now.day, 15, 0, 0, tzinfo=tz) + timedelta(days=timedelta_day)
        persistence_seconds = int((expire_by - now).total_seconds())
        return persistence_seconds
