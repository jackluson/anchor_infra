
import redis
from infra.config.env import env_redis_db, env_redis_host, env_redis_port


class BaseRedis(object):
    client:redis.Redis = None
    def __init__(self):
        self.client = redis.Redis(host=env_redis_host, port=env_redis_port, db=env_redis_db)


