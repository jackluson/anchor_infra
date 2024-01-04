from datetime import datetime, timedelta, timezone
from infra.db.mongo import init_client
from pymongo.collection import Collection
from pymongo.collation import Collation
from pymongo.database import Database
import pymongo
import pytz


class HoldersModel(object):
    client: pymongo.MongoClient = None
    db: Database = None
    collection: Collection = None
    def __init__(self):
        self.client = init_client()
        
        db = self.client['anchor_plan']
        self.db = db
        self.collection = self.db.holders
    def find(self, *args, **kwargs):
        return list(self.collection.find(*args, **kwargs))

    def get_latest_certains_group_stocks(self, groups):
        tz=pytz.timezone('Asia/Shanghai')
        now = datetime.now(tz=tz)

        # Get the start of the day
        day_of_week = now.weekday()
        if day_of_week == 5:
            start_of_day = datetime(now.year, now.month, now.day, 0, 0, 0) - timedelta(days=1)
        elif day_of_week == 6:
            start_of_day = datetime(now.year, now.month, now.day, 0, 0, 0) - timedelta(days=2)
        else:
            start_of_day = datetime(now.year, now.month, now.day, 0, 0, 0)

        # Get the end of the day
        end_of_day = (start_of_day + timedelta(days=1) - timedelta(seconds=1))
        # res = tzlocal.get_localzone()
        # print("res", res)
        holder_model = HoldersModel()
        start_utc = start_of_day.astimezone(timezone.utc)
        # print("start_utc", start_utc)
        # start_utc_1 = start_of_day.now(tz=timezone.utc)
        # start_utc_2 = start_of_day.utcnow()
        end_utc = end_of_day.astimezone(timezone.utc)
        # print("end_utc", end_utc)
        holder_list = holder_model.find({
            "updated_time": {
                "$gte": start_utc,
                "$lte": end_utc,
            },
            "portfolio_name": {
                "$in": groups
            }
        }, {'_id': 0, 'updated_time': 0, 'created_time': 0})
        return holder_list
