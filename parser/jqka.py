'''
Desc:
File: /infra/parser/jqka.py
File Created: Wednesday, 13th September 2023 12:49:56 am
Author: luxuemin2108@gmail.com
-----
Copyright (c) 2023 Camel Lu
'''

from bs4 import BeautifulSoup
import pandas as pd

import time
from infra.parser.base import BaseParser
from infra.utils.index import get_symbol_by_code


def to_number(s):
    try:
        n = float(s)
        return n
    except ValueError:
        pass
    return s


class JqkaParser(BaseParser):

    def __init__(self):
        origin = 'http://basic.10jqka.com.cn'
        self.origin = origin
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,pt;q=0.7,zh-TW;q=0.6',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': '__bid_n=183ba96fe42c3f82e44207; FEID=v10-1eebcea39886b8db33b2c67e20c985693c313e66; __xaf_fpstarttimer__=1672040247475; __xaf_thstime__=1672040247660; __xaf_fptokentimer__=1672040247764; searchGuide=sg; BAIDU_SSP_lcr=https://www.baidu.com/link?url=gy66fehjqf5E1TBjyUnMBP2MMJppbmUSPaDUhWMZ1Dh6M6gp-cPYH0NOVreHsaoC&wd=&eqid=e0d48456001656090000000263c38a62; FPTOKEN=SPfEU6LsmHtpSpi70KZ+SxQ3iSu56rZaQ7L4IpnQIdJVHiR10n+JX3m5d7tY8AzpGAVly+9VdEUfhjKKsnJgfBYFm49D039+LW6Lwz5VxZ1YIo43t8MglD/78ugDQwA0yyqbhvPGXn9e8krZXIY8SDvFh0Gz/9Idldo9M1ZHsr/3Ndt2clDOHANZVqNSZWr2KoyNCBFfFnmBkppl276OwMmt4CflKpKJYHLmRUJ9k4CzG8ivw/WApHQ8etvR7bd/NvP1lQzicqCqrcBQRUHMI1CMxUQfDVmyGyji+n4XVq6W6OIb8FzOe+w/hOp+87WC3PBvrKOeTvrPjlE39vvhHOCEpgv77IoWOgHBVdLggzPzjzXo7ITC3lowX+OaokGWuPMZQ/CXHub6Wbw+NYOgzA==|04kWDFOnxrfrTIBhx17eFzAOZpOyERqM48ui8RT41G4=|10|c3c72fe21fd5b6b9a924acd67067e276; __utma=156575163.1422871151.1663752822.1663752822.1673759342.2; __utmc=156575163; __utmz=156575163.1673759342.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1672712372,1673338870; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1675160025; v=A8uZVqyDLGSLxHCw722O675vXGSwYN_iWXSjlj3Ip4phXOUaxTBvMmlEM-dO',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        }
        super().__init__()

    def get_source(self, url):
        response = self.session.get(
            url=url, headers=self.headers, verify=False)
        response.encoding = 'gbk'
        html = response.text
        return html

    def get_holder_list(self, code):
        market_code = '32' if get_symbol_by_code(code).upper()[:2] == 'SZ' else 16
        ths_detail_url = f"{self.origin}/{market_code}/{code}/detail.html"

        html = self.get_source(ths_detail_url)
        soup = BeautifulSoup(html, "html.parser")
        if not soup.select('div.m_tab_content2.clearfix'):
            return None
        t_date = soup.select('div.m_tab_content2.clearfix')[0].get('id')[2:]
        # 最新一期数据
        rows_latest = soup.select('div.m_tab_content2.clearfix')[
            0].select('table > tbody > tr')
        holder_info_list = []
        for row in rows_latest:
            holder_info = dict()
            keys = ['name', 'type', 'amount', 'radio']
            for i in range(0, 4):
                holder_info[keys[i]] = to_number(row.select('td')[i].text)
            holder_info['date'] = t_date
            holder_info_list.append(holder_info)
        return holder_info_list


if __name__ == '__main__':
    market = 'sz'
    code = '123207'
    parser = JqkaParser()
    holder_list = parser.get_holder_list(code, market)
    df_holder_list = pd.DataFrame(holder_list)
    df_holder_list = df_holder_list.loc[(df_holder_list['radio'] > 5)]
    df_holder_list = df_holder_list.sort_values(
        by='radio', ascending=False, ignore_index=True)
    print('total: ', df_holder_list['radio'].sum())
    print(df_holder_list)
