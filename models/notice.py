'''
Desc:
File: /notice.py
File Created: Saturday, 24th June 2023 9:04:30 pm
Author: luxuemin2108@gmail.com
-----
Copyright (c) 2023 Camel Lu
'''
from db.engine import get_engine
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
    target_time = Column(DateTime, nullable=False, comment='公告日期')
    publish_time = Column(DateTime, nullable=False, comment='公告日期')
    attach_url = Column(String(12), nullable=False, comment='附件链接')

    def __init__(self, **kwargs):
        self.id = idWorker.get_id()
        ORM_Base.__init__(self, **kwargs)
        Model.__init__(self, **kwargs, id=self.id)

    def __repr__(self):
        return f"notice(id={self.id!r}, code={self.title!r})"

    def __init__(self, **kwargs):
        self.id = idWorker.get_id()
        ORM_Base.__init__(self, **kwargs)
        Model.__init__(self, **kwargs, id=self.id)

    def __repr__(self):
        return f"EtfIndicator(id={self.id!r}, code={self.code!r}, name={self.name!r})"


def create():
    # Notice.__table__.drop(engine)
    ORM_Base.metadata.create_all(engine)
    # mapper_registry.metadata.create_all(engine)


def drop():
    Notice.__table__.drop(engine)


if __name__ == '__main__':
    create()
