# -*- coding: utf-8 -*-

from sqlalchemy import Column, Date, Integer, Text

from database import Base
from models import CascadeForeignKey, Table
from utils.hstore import Hstore


class BillProcess(Table, Base):
    __tablename__ = 'bill_process'

    id = Column(Integer, autoincrement=True, primary_key=True)
    bill_id = Column(Text, CascadeForeignKey('bill.id'), nullable=False,
            index=True, unique='uix_bill_process_1')
    status_id = Column(Integer, CascadeForeignKey('bill_status.id'), nullable=False,
            index=True, unique='uix_bill_process_1')

    order = Column(Integer, index=True)
    start_date = Column(Date, index=True)
    end_date = Column(Date, index=True)
    # TODO: 소관위원회 등. 어떤 데이터가 있을까?
    extra_vars = Column(Hstore, nullable=False, default={})


bill_process = BillProcess.__table__

