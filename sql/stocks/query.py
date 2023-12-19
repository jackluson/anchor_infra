'''
Desc: query 相关语句
File: /query.py
Project: sql_model
File Created: Friday, 11th June 2021 12:59:09 pm
Author: luxuemin2108@gmail.com
-----
Copyright (c) 2021 Camel Lu
'''
from datetime import datetime
from ..base import BaseSqlModel


class StockQuery(BaseSqlModel):
    def __init__(self):
        super().__init__()

    def query_industry_data(self):
        query_industry_sql = "SELECT a1.industry_name AS '三级行业', a1.industry_code as '三级行业代码', a2.industry_name AS '二级行业',a2.industry_code as '二级行业代码', a3.industry_name AS '一级行业', a3.industry_code as '一级行业代码' FROM shen_wan_industry as a1 \
        LEFT JOIN shen_wan_industry as a2 ON a2.industry_code = a1.p_industry_code \
            LEFT JOIN shen_wan_industry as a3 ON a3.industry_code = a2.p_industry_code \
            WHERE a1.industry_type=2 AND a2.industry_type=1 AND a3.industry_type = 0"
        self.cursor.execute(query_industry_sql)
        results = self.cursor.fetchall()
        return results
# SELECT * FROM shen_wan_industry as a WHERE a.industry_type = '1' AND a.p_industry_code = 'S22' ORDER BY a.p_industry_code
    def query_shen_wan_industry(self, type=0, p_industry_code='S'):
        query_industry_sql = f"SELECT * FROM shen_wan_industry as a WHERE a.industry_type = '%s' AND a.p_industry_code = %s ORDER BY a.p_industry_code"
        self.dict_cursor.execute(query_industry_sql, [type, p_industry_code])
        results = self.dict_cursor.fetchall()
        return results

    def query_all_stock(self, date=None, *, exclude_table = 'stock_daily_info', date_key = 'timestamp'):
        if date == None:
            query_stock_sql = "SELECT stock_code, stock_name, industry_name_first, industry_name_second, industry_name_third FROM stock_industry WHERE delist_status NOT IN (1) ORDER BY industry_code_first DESC, industry_code_second DESC, industry_code_third DESC"
            self.dict_cursor.execute(query_stock_sql)
        else:
            query_stock_sql = f"SELECT stock_code, stock_name FROM stock_industry as a WHERE a.delist_status = 0 and a.stock_code NOT IN ( SELECT b.`code` FROM {exclude_table} AS b WHERE b.`{date_key}` = %s ) ORDER BY industry_code_first DESC, industry_code_second DESC, industry_code_third DESC"
            self.dict_cursor.execute(query_stock_sql, [date])

        results = self.dict_cursor.fetchall()
        return results

    def query_stock_with_st(self):
        query_stock_sql = "SELECT t.stock_code, t.stock_name, t.industry_name_third, t1.org_name, t1.actual_controller, t1.classi_name, t1.main_operation_business FROM stock_industry as t \
LEFT JOIN stock_profile as t1 ON t.stock_code = t1.stock_code WHERE t.stock_name LIKE '%ST%' AND t.stock_name NOT LIKE '%B%' AND t.delist IS NULL"
        self.dict_cursor.execute(query_stock_sql)
        results = self.dict_cursor.fetchall()
        return results

    def query_stock_by_code(self, code: str):
        query_stock_sql = "SELECT t.stock_name, t.industry_name_third, t.industry_name_second, t.industry_name_first, t1.org_name, t1.actual_controller, t1.classi_name, t1.main_operation_business FROM stock_industry as t \
LEFT JOIN stock_profile as t1 ON t.stock_code = t1.stock_code WHERE t.`stock_code` = %s AND t.delist IS NULL"
        self.dict_cursor.execute(query_stock_sql, [code])
        results = self.dict_cursor.fetchone()
        return results

    def query_stock_main_financial(self, *, code=None, report_date):
        """ 查看股票主要财务数据
        """
        if code:
            query_stock_sql = "SELECT a.* FROM stock_main_financial_indicator as a WHERE a.code = %s AND a.report_date = %s"
            self.dict_cursor.execute(query_stock_sql, [code, report_date])
        else:
            query_stock_sql = "SELECT a.* FROM stock_main_financial_indicator as a WHERE a.report_date = %s"
            self.dict_cursor.execute(query_stock_sql, [report_date])

        results = self.dict_cursor.fetchall()
        return results

    def query_etf(self, found_date=None):
        """
        查询ETF
        Args:
            market ([str]): ['sh', 'sz']
        """
        found_date = found_date if found_date else datetime.now().strftime("%Y-%m-%d")
        query_stock_sql = "SELECT a.code, a.name, a.market FROM etf_fund as a WHERE a.delist_date IS NULL AND a.found_date <= %s"
        self.dict_cursor.execute(query_stock_sql, [found_date])

        results = self.dict_cursor.fetchall()
        return results

    def query_stock_quote(self, date=None):
        if date == None:
            query_stock_sql = "SELECT * FROM stock_daily_info as a LEFT JOIN stock_profile as b ON b.stock_code = a.`code`"
            self.dict_cursor.execute(query_stock_sql)
        else:
            query_stock_sql = "SELECT * FROM stock_daily_info as a LEFT JOIN stock_profile as b ON b.stock_code = a.`code` LEFT JOIN stock_industry as c ON c.stock_code = a.code WHERE a.status=1 and a.`timestamp` = %s"
            self.dict_cursor.execute(query_stock_sql, [date])

        results = self.dict_cursor.fetchall()
        return results
    
    def query_stock_pe_pb(self, date=None):
        query_stock_sql = "SELECT * FROM stock_pe_pb as a LEFT JOIN stock_profile as b ON b.stock_code = a.`code` WHERE a.`date` = %s"
        self.dict_cursor.execute(query_stock_sql, [date])

        results = self.dict_cursor.fetchall()
        return results

    def query_all_stock_belong_provinces(self):
        query_sql = "SELECT a.provincial_name, COUNT(*) as count FROM stock_profile as a GROUP BY a.provincial_name ORDER BY COUNT(*) DESC"
        self.dict_cursor.execute(query_sql)
        results = self.dict_cursor.fetchall()
        return results
    
    def query_stock_name(self, stocks):
        stocks_str = ",".join(f'"{stock}"' for stock in stocks)
        query_sql = f"SELECT stock_code, stock_name from stock_industry WHERE stock_code in ({stocks_str})"
        self.dict_cursor.execute(query_sql)
        results = self.dict_cursor.fetchall()
        return results
