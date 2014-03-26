from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table

from pokr.database import Base


cosponsorship = Table('cosponsorship', Base.metadata,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('person_id', Integer, ForeignKey('person.id'), nullable=False),
    Column('bill_id', String(20), ForeignKey('bill.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
    Column('is_sponsor', Boolean, default=False, index=True),
)

