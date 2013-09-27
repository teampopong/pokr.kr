# -*- coding: utf-8 -*-

from sqlalchemy import Column, Float, Integer, Text
from sqlalchemy.orm import relationship

from database import Base
from models import CascadeForeignKey, Table


class BillKeyword(Table, Base):
    __tablename__ = 'bill_keyword'

    id = Column(Integer, autoincrement=True, primary_key=True)
    bill_id = Column(Text, CascadeForeignKey('bill.id'), nullable=False,
            index=True, unique='uix_bill_keyword_1')
    keyword_id = Column(Integer, CascadeForeignKey('keyword.id'),
            nullable=False, index=True, unique='uix_bill_keyword_1')
    weight = Column(Float, default=1, nullable=False, index=True)

    ### Relations ###
    bill = relationship('Bill', uselist=False)
    keyword = relationship('Keyword', uselist=False)


bill_keyword = BillKeyword.__table__

