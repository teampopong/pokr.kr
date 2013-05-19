# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, Unicode

from database import Base


class BillStatus(Base):
    __tablename__ = 'bill_status'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Unicode(150), index=True, nullable=False)
