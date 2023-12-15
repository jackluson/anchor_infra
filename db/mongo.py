from pymongo import MongoClient
from ..config.env import env_mongodb_url

def init_client():
   client = MongoClient(env_mongodb_url)
   return client
