from sqlalchemy import Column, ForeignKey, Integer, String, Table

from pokr.database import Base


bill_withdrawal = Table('bill_withdrawal', Base.metadata,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('person_id', Integer, ForeignKey('person.id'), nullable=False),
    Column('bill_id', String(20), ForeignKey('bill.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
)

