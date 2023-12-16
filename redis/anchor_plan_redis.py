import json
from infra.redis.base import BaseRedis

_global_redis = None

class AnchorPlanRedis(BaseRedis):
    def __init__(self):
        super().__init__()
        self.mongo_cur_holder_list_key = 'mongo#cur_holder_list'
        self.mongo_cur_care_list_key = 'mongo#cur_care_list'
    def set_with_dumps(self, key, value, expire=2 * 60 * 60):
        encoded_data = json.dumps(value)
        self.client.set(key, encoded_data, 2 * 60 * 60)
    def get_with_loads(self, key):
        res = self.client.get(key)
        if res:
        # Retrieve the data from Redis and decode it using json.loads
          decoded_data = json.loads(res)
          return decoded_data
    def set_cur_holder_list(self, holder_list, expire=2 * 60 * 60 ):
        return self.set_with_dumps(self.mongo_cur_holder_list_key, holder_list, expire)
    def get_cur_holder_list(self):
        return self.get_with_loads(self.mongo_cur_holder_list_key)
    def set_cur_care_list(self, holder_list, expire=2 * 60 * 60 ):
        return self.set_with_dumps(self.mongo_cur_care_list_key, holder_list, expire)
    def get_cur_care_list(self):
        return self.get_with_loads(self.mongo_cur_care_list_key)


def create_singleton_anchor_plan_redis():
    global _global_redis
    if not _global_redis:
        _global_redis = AnchorPlanRedis()
    return _global_redis
  
def get_anchor_plan_redis():
    return create_singleton_anchor_plan_redis()
# def cache()
