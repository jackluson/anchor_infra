from infra.redis.base import BaseRedis

_global_redis = None
class AnchorPlanRedis(BaseRedis):
    def __init__(self):
        super().__init__()
        self.mongo_cur_holder_list_key = 'mongo#cur_holder_list'
        self.mongo_cur_care_list_key = 'mongo#cur_care_list'

        self.convertible_bond_filter_listed_all_key = 'convertible_bond#filter_listed_all'
        self.convertible_bond_filter_listed_all_exclude_new = 'convertible_bond#filter_listed_all_exclude_new'
        self.convertible_bond_filter_double_low_key = 'convertible_bond#filter_double_low'
        self.convertible_bond_filter_multiple_factors_key = 'convertible_bond#filter_multiple_factors'
        self.convertible_bond_filter_low_level_stock_key = 'convertible_bond#filter_low_level_stock'
        self.convertible_bond_filter_genie_key = 'convertible_bond#filter_genie'
        self.convertible_bond_filter_small_scale_not_ransom_key = 'convertible_bond#filter_small_scale_not_ransom'
        self.convertible_bond_filter_new_small_key = 'convertible_bond#filter_new_small'
        self.convertible_bond_filter_candidate_key = 'convertible_bond#filter_candidate'
        self.convertible_bond_filter_downward_revise_key = 'convertible_bond#filter_downward_revise'
        self.convertible_bond_filter_profit_due_key = 'convertible_bond#filter_profit_due'
        self.convertible_bond_filter_return_lucky_key = 'convertible_bond#filter_return_lucky'

        self.convertible_bond_stats_info_key = 'convertible_bond#stats_info'

    def set_cur_holder_list(self, holder_list, expire=2 * 60 * 60 ):
        return self.set_with_dumps(self.mongo_cur_holder_list_key, holder_list, expire)
    def get_cur_holder_list(self):
        return self.get_with_loads(self.mongo_cur_holder_list_key)
    def set_cur_care_list(self, holder_list, expire=2 * 60 * 60 ):
        return self.set_with_dumps(self.mongo_cur_care_list_key, holder_list, expire)
    def get_cur_care_list(self):
        return self.get_with_loads(self.mongo_cur_care_list_key)

    def set_filter_listed_all(self, listed_all, expire=2 * 60 * 60 ):
        return self.set_with_dumps(self.convertible_bond_filter_listed_all_key, listed_all, expire)

    def get_filter_listed_all(self):
        return self.get_with_loads(self.convertible_bond_filter_listed_all_key)

    def set_convertible_bond_filter_result(self, key, value, *, full_key=None):
        full_key = 'convertible_bond#' + key
        persistence_seconds = self.get_expire_seconds_based_quote()
        return self.set_with_dumps(full_key, value, expire=persistence_seconds)
    def get_convertible_bond_filter_result(self, key=None, *, full_key=None):
        full_key = full_key if full_key else 'convertible_bond#' + key
        return self.get_with_loads(full_key)
    
    def set_convertible_bond_stats_info(self, title, value, *, full_key=None):
        full_key = full_key if full_key else f'convertible_bond#stats_info_{title}'
        persistence_seconds = self.get_expire_seconds_based_quote()
        return self.hset(full_key, mapping=value, expire=persistence_seconds)
    def get_convertible_bond_stats_info(self, title=None, *, full_key=None, field:str=None):
        full_key = full_key if full_key else f'convertible_bond#stats_info_{title}'
        if field:
            return self.hget(full_key, field)
        else:
            return self.hgetall(full_key)

def create_singleton_anchor_plan_redis():
    global _global_redis
    if not _global_redis:
        _global_redis = AnchorPlanRedis()
    return _global_redis
  
def get_anchor_plan_redis():
    return create_singleton_anchor_plan_redis()
