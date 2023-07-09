'''
Desc:
File: /notice.py
File Created: Saturday, 24th June 2023 9:04:30 pm
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


class Notice(ORM_Base, Model):
    __tablename__ = 'notice'
    __table_args__ = {'extend_existing': True}
    id = Column(BigInteger, primary_key=True)
    title = Column(String(48), nullable=False, comment='公告标题')
    name = Column(String(24), nullable=False, comment='名称')
    code = Column(String(12), nullable=False, comment='代码')
    type = Column(String(12), nullable=False, comment='类型')
    type_code = Column(String(24), nullable=False, comment='类型编码')
    target_time = Column(DateTime, nullable=False, comment='公告日期')
    publish_time = Column(DateTime, nullable=False, comment='公告日期')
    attach_url = Column(String(108), nullable=False, comment='附件链接')
    
    update_time = Column(DateTime,  server_default=text(
        'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), onupdate=func.now(), comment='更新时间')
    create_time = Column(DateTime, server_default=text(
        'CURRENT_TIMESTAMP'), comment='创建时间')
    UniqueConstraint(title, target_time, name='uix_1')
    def __init__(self, **kwargs):
        self.id = idWorker.get_id()
        ORM_Base.__init__(self, **kwargs)
        Model.__init__(self, **kwargs, id=self.id)

    def __repr__(self):
        return f"notice(id={self.id!r}, code={self.title!r})"

    @staticmethod
    def bulk_save(data_list: list, ignore_key=[]):
        """批量保存(新增或者更新, id只能是新增)

        Args:
            data_list (list): _description_
        """
        ups_stmt = insert(Notice).values(
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
    table = ORM_Base.metadata.tables[Notice.__tablename__]
    if table is not None:
        Notice.__table__.drop(engine)
    ORM_Base.metadata.create_all(engine)
    # mapper_registry.metadata.create_all(engine)


def drop():
    Notice.__table__.drop(engine)


if __name__ == '__main__':
    create()
