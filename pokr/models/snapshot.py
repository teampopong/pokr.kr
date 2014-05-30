# -*- coding: utf-8 -*-

from datetime import date

from sqlalchemy import Column, Date, Integer, Text
from sqlalchemy.dialects.postgresql import JSON

from pokr.database import Base


__all__ = ['Snapshot']


class Snapshot(Base):
    __tablename__ = 'snapshot'

    id = Column(Integer, autoincrement=True, primary_key=True)
    tablename = Column(Text, index=True, nullable=False)
    record_id = Column(Text, index=True, nullable=False)
    date = Column(Date, index=True, default=date.today)
    data = Column(JSON)

