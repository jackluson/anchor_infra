from infra.redis.anchor_plan_redis import AnchorPlanRedis, get_anchor_plan_redis
from infra.collections.holders import HoldersModel

class HoldersMemory(object):
    redis: AnchorPlanRedis = None
    model: HoldersModel = None
    def __init__(self) -> None:
        self.redis = get_anchor_plan_redis
        self.model = HoldersModel()

    def get_latest_certains_group_stocks(self, groups, is_holders_key):
        redis = self.redis
        redis_result = redis.get_cur_holder_list() if is_holders_key else redis.get_cur_care_list()
        if redis_result:
            return redis_result
        holder_list = self.model.get_latest_certains_group_stocks(groups)
        if is_holders_key:
            redis.set_cur_holder_list(holder_list)
        else:
            redis.set_cur_care_list(holder_list)
        return holder_list
