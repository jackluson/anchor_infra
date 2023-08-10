'''
Desc:
File: /jisilu.py
File Created: Sunday, 19th March 2023 10:21:33 pm
Author: luxuemin2108@gmail.com
-----
Copyright (c) 2022 Camel Lu
'''
import time
import json
import requests
import os
from .base import BaseApier
from ..utils.file import write_fund_json_data


class ApiJiSiLu(BaseApier):
    def __init__(self):
        origin = 'https://www.jisilu.cn'
        referer = 'https://www.jisilu.cn/data/stock/dividend_rate/'
        self.origin=origin
        super().__init__()
        self.set_client_headers(
            cookie_env_key="jisilu_cookie", referer=referer, origin=origin, )

    def get_last_indicator(self):
        url = f"{self.origin}/data/indicator/get_last_indicator/"
        data = self.post(url)
        return data

    def get_pre_list(self, *, history="N"):
        cur_date = time.strftime(
            "%Y-%m-%d", time.localtime(time.time()))
        file_dir = os.getcwd() + f'/data/json/jisilu/'
        filename = 'pre_' + cur_date + '.json'
        is_exist = os.path.exists(file_dir + filename)
        if is_exist:
            with open(file_dir + filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        url = f"{self.origin}/webapi/cb/pre/?history={history}"
        data = self.post(url).get('data')
        write_fund_json_data(data, filename, file_dir)
        return data

    def get_diviend_rate(self, *, industry=None):

        cur_date = time.strftime(
            "%Y-%m-%d", time.localtime(time.time()))
        file_dir = os.getcwd() + f'/data/json/jisilu/{cur_date}/'
        filename = industry + '.json'
        is_exist = os.path.exists(file_dir + filename)
        if is_exist:
            with open(file_dir + filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        url = f"{self.origin}/data/stock/dividend_rate_list/?___jsl=LST___t=1679235660274"
        payload = {
            "market[]": "sh",
            "market[]": "sz",
            "industry": industry,
            "rp": 500
        }
        res = requests.post(url, data=payload, headers=self.headers)
        try:
            if res.status_code == 200:
                res_json = res.json()
                write_fund_json_data(res_json.get("rows"), filename, file_dir)
                return res_json.get("rows")
        except:
            raise ('请求异常')
