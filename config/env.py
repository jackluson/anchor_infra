'''
Desc:
File: /config.py
Project: config
File Created: Sunday, 14th August 2022 5:57:02 pm
Author: luxuemin2108@gmail.com
-----
Copyright (c) 2022 Camel Lu
'''
import os
from os.path import join, dirname

from dotenv import load_dotenv
dotenv_path = join(os.getcwd(), '.env')
load_dotenv(dotenv_path=dotenv_path)

env_db_host = os.getenv('db_host')
env_db_port = os.getenv('db_port')
env_db_name = os.getenv('db_name')
env_db_user = os.getenv('db_user')
env_db_password = os.getenv('db_password')
env_mongodb_url = os.getenv("MONGODB_URI")

env_redis_host = os.environ.get('REDIS_HOST', '127.0.0.1')
env_redis_port = int(os.environ.get('REDIS_PORT', 6379))
env_redis_db = int(os.environ.get('REDIS_DB', 0))
env_redis_password = os.environ.get('REDIS_PASSWORD', None)
