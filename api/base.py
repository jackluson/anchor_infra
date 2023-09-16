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
from dotenv import load_dotenv
import requests
from functools import wraps
from ..utils.file import write_fund_json_data

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class BaseApier:
    headers = dict()

    session: requests.Session = None
    _logger: logging = None

    def __init__(self):
        load_dotenv()
        session = requests.Session()
        retry = Retry(connect=6, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        self.session = session

    def init_loger(self):
        # 1、创建一个logger
        logger = logging.getLogger('apilogger')
        logger.setLevel(logging.DEBUG)

        # 2、创建一个handler，用于写入日志文件
        fh = logging.FileHandler('log/api.log')
        fh.setLevel(logging.DEBUG)

        # # 再创建一个handler，用于输出到控制台
        # ch = logging.StreamHandler()
        # ch.setLevel(logging.DEBUG)

        # 3、定义handler的输出格式（formatter）
        formatter = logging.Formatter(
            '%(levelname)s - %(asctime)s - %(name)s -  %(filename)s[line:%(lineno)d] - %(message)s')

        # 4、给handler添加formatter
        fh.setFormatter(formatter)
        # ch.setFormatter(formatter)
        if not logger.handlers:
            # 5、给logger添加handler
            logger.addHandler(fh)
        self._logger = logger
        # logger.addHandler(ch)
        return logger

    @property
    def logger(self) -> logging:
        if self._logger == None:
            self.init_loger()
            return self._logger
        else:
            self._logger

    @classmethod
    def GetLogger(cls):
        return cls().logger

    def set_client_headers(self, *,  cookie_env_key="xue_qiu_cookie", referer="https://xueqiu.com", origin=None):
        cookie = self.__dict__.get(cookie_env_key)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36',
            'Origin': origin if origin else referer,
            'Referer': referer if referer else self.referer,
            'Cookie': cookie,
        }
        self.headers = headers
        return headers

    def get(self, url, **kwargs):
        # self.logger.info(f'host:{self.__dict__.get("base_url")}')
        # self.logger.error(f'host:{self.__dict__.get("base_url")}')
        response = self.session.get(url, headers=self.headers, **kwargs)
        try:
            if response.status_code == 200:
                return response.json()
        except:
            raise ('请求异常')

    def post(self, url, **kwargs):
        merge_header = {
            **self.headers,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = self.session.post(url, headers=merge_header, **kwargs)
        try:
            if response.status_code == 200:
                return response.json()
        except:
            raise ('请求异常')

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
    def Cache(path, cache_key_position=1, *, use_cache=True):
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
                        # BaseApier.init_loger().critical(e, exc_info=True)
                        logger = BaseApier.GetLogger()
                        logger.exception(e)
                        return fn()
                else:
                    return func(*args, **kwargs)
            return wrapper
        return _log
