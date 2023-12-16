from datetime import datetime
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
