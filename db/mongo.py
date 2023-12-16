import pytz
from pymongo import MongoClient
from ..config.env import env_mongodb_url

tzinfo = pytz.timezone('Asia/Shanghai')

def init_client():
   client = MongoClient(env_mongodb_url, tz_aware=True, tzinfo=tzinfo)
   return client
