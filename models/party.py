# -*- coding: utf-8 -*-

from sqlalchemy import CHAR, Column, Date, Integer, Text
from sqlalchemy.orm import deferred

from database import Base
from models import Table


class Party(Table, Base):
    __tablename__ = 'party'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text, nullable=False, index=True)

    start_date = Column(Date, index=True)
    end_date = Column(Date, index=True)
    logo = deferred(Column(Text), group='extra')
    color = deferred(Column(CHAR(6)), group='extra')
    homepage = deferred(Column(Text), group='extra')

