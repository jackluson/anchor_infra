'''
Desc:
File: /base.py
File Created: Sunday, 9th July 2023 10:10:31 am
Author: luxuemin2108@gmail.com
-----
Copyright (c) 2023 Camel Lu
'''
import logging
import os
import json
from datetime import datetime
from fake_useragent import UserAgent
import pandas as pd
from dotenv import load_dotenv
import requests
from functools import wraps
# from infra.cache.beaker import cache, create_cache, EndMode
from infra.utils.index import timeit
from infra.logger.logger import error_logger, Logger
from ..utils.file import write_fund_json_data

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class BaseApier:
    headers = dict()
    logger = Logger(file='log/api.log', logger_format=" [%(asctime)s]  %(levelname)s %(message)s",  show_stream=False)
    session: requests.Session = None

    def __init__(self):
        load_dotenv()
        session = requests.Session()
        retry = Retry(connect=6, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        self.session = session

    def get_cookie(self, url):
        self.get_html(url)
        cookie_dict = self.session.cookies.get_dict()
        cookie_str = ''
        for key, val in cookie_dict.items():
            cookie_str = f"{cookie_str}{key}={val}; "
        cookie_str = cookie_str[0:-2]
        return cookie_str

    def set_client_headers(self, *, cookie_env_key=None, referer, origin=None):
        cookie = self.__dict__.get(cookie_env_key, os.getenv(cookie_env_key))
        referer = referer if referer else self.__dict__.get("referer")
        ua = UserAgent()
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
            'User-Agent': ua.random.lstrip(), # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36',
            'Origin': origin if origin else referer,
            'Referer': referer,
            'Cookie': cookie,
        }
        self.headers = headers
        return headers

    def get(self, url, **kwargs):
        try:
            response = self.session.get(url, headers=self.headers, **kwargs)
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.exception(response)
        except BaseException as e:
            error_logger.error(f'error url:{url}')
            if len(kwargs.keys()):
                error_logger.error(kwargs)
            error_logger.exception(e)
            raise Exception('fetch error', url, kwargs)

    def get_html(self, url, **kwargs):
        ua = UserAgent()
        headers = {
            'User-Agent': ua.random.lstrip(),
            **self.headers,
           'Content-Type': 'text/html; charset=utf-8'
        }
        try:
            res = self.session.get(url, headers=headers, **kwargs)
            print("本次请求使用的cookie：",res.request.headers.get("Cookie"))
            if res.status_code == 200:
                return res.text
            else:
                self.logger.exception(res)
        except BaseException as e:
            error_logger.error(f'error url:{url}')
            if len(kwargs.keys()):
                error_logger.error(kwargs)
            error_logger.exception(e)
            raise Exception('fetch error', url, kwargs)

    def post(self, url, **kwargs):
        merge_header = {
            **self.headers,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        try:
            response = self.session.post(url, headers=merge_header, **kwargs)
            if response.status_code == 200:
                return response.json()
        except BaseException as e:
            error_logger.error(f'error url:{url}')
            if len(kwargs.keys()):
                error_logger.error(kwargs)
            error_logger.exception(e)
            raise Exception('fetch error', url, kwargs)

    @staticmethod
    def Log(arg):
        def _log(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                print('log开始 ...', func.__name__, arg)
                ret = func(*args, **kwargs)
                print('log结束 ...')
                return ret
            return wrapper
        return _log

    @staticmethod
    def CacheJSON(path, cache_key_position=1, *, use_cache=True):
        def _log(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if use_cache:
                    cache_key = None
                    if type(cache_key_position) == int:
                        cache_key = args[cache_key_position]
                    elif type(cache_key_position) == str:
                        cache_key = kwargs.get(cache_key_position)
                    file_dir = os.getcwd() + path + '/'
                    cache_filename_path = f"{cache_key}.json"
                    fullpath = f"{file_dir}{cache_filename_path}"
                    is_exist = os.path.exists(fullpath)

                    def fn():
                        data = func(*args, **kwargs)
                        write_fund_json_data(
                            data, cache_filename_path, file_dir)
                        return data
                    try:
                        if is_exist:
                            with open(fullpath, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                                return data
                        else:
                            return fn()
                    except Exception as e:
                        return fn()
                else:
                    return func(*args, **kwargs)
            return wrapper
        return _log

    # @staticmethod
    # def Cache(*args, **kwargs):
    #     return create_cache(*args, **kwargs)
