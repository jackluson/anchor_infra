'''
Desc:
File: /pe_pb.py
Project: models
File Created: Thursday, 2nd November 2023 5:01:25 pm
Author: luxuemin2108@gmail.com
-----
Copyright (c) 2023 Camel Lu
'''

from sqlalchemy.dialects.mysql import insert
from ..db.engine import get_engine
from .var import ORM_Base, Model, idWorker
from sqlalchemy import (UniqueConstraint, ForeignKey, Table,
                        String, Float, Column, text, DateTime, BigInteger, func)

engine = get_engine()

class Stock_PE_PB(ORM_Base, Model):
    __tablename__ = 'stock_pe_pb'
    __table_args__ = {'extend_existing': True}
    id = Column(BigInteger, primary_key=True)
    name = Column(String(24), nullable=False, comment='名称')
    code = Column(String(12), nullable=False)
    date = Column(DateTime, nullable=False, comment='日期')
    pb = Column(Float, nullable=True, comment='pb 值')
    pb_mid = Column(Float, nullable=True, comment='pb 中位数 默认十年')
    pb_mid_1 = Column(Float, nullable=True, comment='pb 中位数 1年')
    pb_mid_3 = Column(Float, nullable=True, comment='pb 中位数 3年')
    pb_mid_5 = Column(Float, nullable=True, comment='pb 中位数 5年')
    pb_mid_all = Column(Float, nullable=True, comment='pb 所有时间')
    
    pb_percent = Column(Float, nullable=True, comment='pb 百分位 默认十年')
    pb_percent_1 = Column(Float, nullable=True, comment='pb 百分位(1年期间) ')
    pb_percent_3 = Column(Float, nullable=True, comment='pb 百分位(3年期间) ')
    pb_percent_5 = Column(Float, nullable=True, comment='pb 百分位(5年期间) ')
    pb_percent_all = Column(Float, nullable=True, comment='pb 百分位(所有期间段) ')
    
    pe = Column(Float, nullable=True, comment='pe 值')
    pe_mid = Column(Float, nullable=True, comment='pe 中位数 默认十年时间段')
    pe_mid_1 = Column(Float, nullable=True, comment='pe 中位数 1年')
    pe_mid_3 = Column(Float, nullable=True, comment='pe 中位数 3年')
    pe_mid_5 = Column(Float, nullable=True, comment='pe 中位数 5年')
    pe_mid_all = Column(Float, nullable=True, comment='pe 所有时间')

    pe_percent = Column(Float, nullable=True, comment='pe 百分位 默认10年')
    pe_percent_1 = Column(Float, nullable=True, comment='pe 百分位 默认1年')
    pe_percent_3 = Column(Float, nullable=True, comment='pe 百分位 默认3年')
    pe_percent_5 = Column(Float, nullable=True, comment='pe 百分位(5年期间) ')
    pe_percent_all = Column(Float, nullable=True, comment='pe 百分位(所有期间段) ')
    
    pe_koufei = Column(Float, nullable=True, comment='pe_koufei 值')
    pe_koufei_mid = Column(Float, nullable=True, comment='pe_koufei 中位数 默认十年时间段')
    pe_koufei_mid_1 = Column(Float, nullable=True, comment='pe_koufei 中位数 1年')
    pe_koufei_mid_3 = Column(Float, nullable=True, comment='pe_koufei 中位数 3年')
    pe_koufei_mid_5 = Column(Float, nullable=True, comment='pe_koufei 中位数 5年')
    pe_koufei_mid_all = Column(Float, nullable=True, comment='pe_koufei 所有时间')

    pe_koufei_percent = Column(Float, nullable=True, comment='pe_koufei 百分位 默认十年')
    pe_koufei_percent_1 = Column(Float, nullable=True, comment='pe_koufei 百分位(1年期间) ')
    pe_koufei_percent_3 = Column(Float, nullable=True, comment='pe_koufei 百分位(3年期间) ')
    pe_koufei_percent_5 = Column(Float, nullable=True, comment='pe_koufei 百分位(5年期间) ')
    pe_koufei_percent_all = Column(Float, nullable=True, comment='pe_koufei 百分位(所有期间段) ')
    
    update_time = Column(DateTime,  server_default=text(
        'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), onupdate=func.now(), comment='更新时间')
    create_time = Column(DateTime, server_default=text(
        'CURRENT_TIMESTAMP'), comment='创建时间')
    
    UniqueConstraint(code, date, name='uix_1')

    def __repr__(self):
        return f"notice(id={self.id!r}, code={self.name!r})"

    @staticmethod
    def bulk_save(data_list: list, ignore_key=[]):
        if data_list is None or len(data_list) == 0:
            return
        """批量保存(新增或者更新, id只能是新增)

        Args:
            data_list (list): _description_
        """
        ups_stmt = insert(Stock_PE_PB).values(
            data_list
        )
        update_dict = {x.name: x for x in ups_stmt.inserted}
        # del update_dict['id']
        for key in ignore_key:
            del update_dict[key]
        ups_stmt = ups_stmt.on_duplicate_key_update(update_dict)
        with engine.connect() as conn:
            conn.execute(ups_stmt)
            conn.commit()



def create():
    table = ORM_Base.metadata.tables.get(Stock_PE_PB.__tablename__)
    if table is not None:
        Stock_PE_PB.__table__.drop(engine)
    ORM_Base.metadata.create_all(engine)
    # mapper_registry.metadata.create_all(engine)


def drop():
    Stock_PE_PB.__table__.drop(engine)


if __name__ == '__main__':
    create()
