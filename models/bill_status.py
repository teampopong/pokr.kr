# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, Text

from database import Base
from models import Table


class BillStatus(Table, Base):
    __tablename__ = 'bill_status'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text, index=True, nullable=False)
    description = Column(Text)

