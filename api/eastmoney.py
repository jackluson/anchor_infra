import time
import json
import os
import random
# from infra.cache.beaker import create_cache, EndMode
from .base import BaseApier

# def create_eastmoney_cache(*, expire=3600, end=EndMode.Day, is_before_clear=False):
#     return create_cache(module="eastmoney", expire=expire, end=end, is_before_clear=is_before_clear)

class ApiEastMoney(BaseApier):
    def __init__(self):
        super().__init__()
        referer = 'http://fundf10.eastmoney.com/'
        self.referer = referer
        self.notice_api_base_url = 'https://np-anotice-stock.eastmoney.com/api'
        self.set_client_headers(cookie_env_key="eastmoney_cookie", referer=referer)

    def get_fund_net_worth(self, *, code, start_date, end_date, page_index, page_size):
        timestamp = int(time.time() * 1000)
        callback = "jQuery18305757733125714872_" + str(timestamp)
        url = "http://api.fund.eastmoney.com/f10/lsjz?callback={callback}&fundCode={code}&pageIndex={page_index}&pageSize={page_size}&startDate={start_date}&endDate={end_date}&_={timestamp}".format(
            callback=callback,
            code=code,
            start_date=start_date,
            end_date=end_date,
            page_index=page_index,
            page_size=page_size,
            timestamp=timestamp
        )
        res = self.session.get(url, headers=self.headers)
        try:
            if res.status_code == 200:
                data_text = res.text.replace(callback, '')[1:-1]
                res_json = json.loads(data_text)
                return res_json
            else:
                print('请求异常', res)
        except:
            raise ('中断')

    # @create_eastmoney_cache(expire=60 * 5, end=None)
    def get_notices_info(self, *, code, page_size, page_index, ann_type):
        timestamp = int(time.time() * 1000)
        callback = "jQuery112308272385073717725_" + str(timestamp)
        url = "{base_url}/security/ann?cb={callback}&sr=-1&page_size={page_size}&page_index={page_index}&pageSize={page_size}&ann_type={ann_type}&client_source=web&stock_list={stock_list}&f_node={f_node}&s_node={s_node}".format(
            base_url=self.notice_api_base_url,
            callback=callback,
            page_size=page_size,
            page_index=page_index,
            ann_type=ann_type,
            stock_list=code,
            f_node=0,
            s_node=1,
        )
        res = self.session.get(url, headers=self.headers)
        try:
            if res.status_code == 200:
                data_text = res.text.replace(callback, '')[1:-1]
                res_json = json.loads(data_text)
                return res_json
            else:
                print('请求异常', res)
        except:
            raise ('中断')

    # @create_eastmoney_cache()
    def get_notice_detail(self, *, art_code):
        timestamp = int(time.time() * 1000)
        # jQuery112302017701812703181_1688868121679
        seed = random.randint(100000, 999999)
        callback = f"jQuery112302017701812{seed}_{str(timestamp)}"
        url = "{base_url}/content/ann?cb={callback}&art_code={art_code}&page_index={page_index}&client_source=web&_{timestamp}".format(
            base_url="https://np-cnotice-stock.eastmoney.com/api",
            callback=callback,
            art_code=art_code,
            page_index=1,
            timestamp=timestamp,
        )
        res = self.session.get(url, headers=self.headers)
        try:
            if res.status_code == 200:
                data_text = res.text.replace(callback, '')[1:-1]
                res_json = json.loads(data_text)
                return res_json
            else:
                print('请求异常', res)
        except:
            raise ('中断')

    # @create_eastmoney_cache()
    def get_all_stocks_with_st(self, *, page_index=1, page_size=200):
        # cur_date = time.strftime(
        #     "%Y-%m-%d", time.localtime(time.time()))
        # file_dir = os.getcwd() + '/data/json/st/'
        # filename = 'st_' + cur_date + '.json'
        # is_exist = os.path.exists(file_dir + filename)
        # if is_exist:
        #     with open(file_dir + filename, 'r', encoding='utf-8') as f:
        #         data = json.load(f)
        #         return data
        timestamp = int(time.time() * 1000)
        callback = "jQuery112405829056173474523_" + str(timestamp)

        url = "http://94.push2.eastmoney.com/api/qt/clist/get?cb={callback}&pn={page_index}&pz={page_size}&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&wbp2u=|0|0|0|web&fid=f3&fs=b:BK0511+f:\u002150&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152,f45&_={timestamp}".format(
            callback=callback,
            page_index=page_index,
            page_size=page_size,
            timestamp=timestamp,
        )
        res = self.session.get(url, headers=self.headers)
        try:
            if res.status_code == 200:
                data_text = res.text.replace(callback, '')[1:-2]
                res_json = json.loads(data_text)
                # write_fund_json_data(res_json.get(
                #     'data').get('diff'), filename, file_dir)
                return res_json.get('data').get('diff')
            else:
                print('请求异常', res)
        except:
            raise ('中断')

    # @create_eastmoney_cache(end=EndMode.Month)
    def get_yzxdr(self, code: str, *, end_date='2023-09-30', retry=True):
        # TODO: end_date 处理
        timestamp = int(time.time() * 1000)
        callback = "jQuery11230688981214770831_" + str(timestamp)
        params = {
            'callback': callback,
            'sortColumns': 'SHAREHDNUM',
            'sortTypes': -1,
            'pageSize': 50,
            'pageNumber': 1,
            'columns': 'ALL',
            'reportName': 'RPTA_WEB_YZXDRXQ',
            'filter': f'(DIM_SCODE="{code}")(ENDDATE=\'{end_date}\')',
        }
        url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
        res = self.session.get(url, params=params,  headers=self.headers)
        try:
            if res.status_code == 200:
                data_text = res.text.replace(callback, '')[1:-2]
                res_json = json.loads(data_text)
                result = res_json.get('result')
                success = res_json.get('success')
                if result and success:
                    return result.get('data')
                else:
                    if retry:
                        return self.get_yzxdr(code, end_date='2023-06-30', retry=False)
                    return []
            else:
                print('请求异常', res)
        except:
            raise ('中断')
