from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.schema import UniqueConstraint
from pokr.database import Base

bill_keyword = Table('bill_keyword', Base.metadata,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('bill_id', String(20), ForeignKey('bill.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
    Column('keyword_id', Integer, ForeignKey('keyword.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
    Column('weight', Float, default=0, nullable=False),
    UniqueConstraint('bill_id', 'keyword_id', name='uix_1'),
)

