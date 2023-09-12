'''
Desc:
File: /infra/parser/base.py
File Created: Wednesday, 13th September 2023 1:05:19 am
Author: luxuemin2108@gmail.com
-----
Copyright (c) 2023 Camel Lu
'''
import requests

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class BaseParser:
    session: requests.Session = None

    def __init__(self):
        session = requests.Session()
        retry = Retry(connect=6, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        self.session = session
