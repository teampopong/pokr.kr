# -*- coding: utf-8 -*-

from sqlalchemy import Boolean, Column, Date, func, Integer, select, String, Unicode
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from database import Base
from models.bill_status import BillStatus


class Bill(Base):
    __tablename__ = 'bill'

    id = Column(String(20), primary_key=True)
    name = Column(Unicode(150), index=True, nullable=False)

    age = Column(Integer, index=True, nullable=False)
    proposed_date = Column(Date, index=True)
    decision_date = Column(Date, index=True)

    is_processed = Column(Boolean, index=True)
    link_id = Column(String(40), index=True)

    status_id = Column(Integer, nullable=False)
    status_ids = Column(ARRAY(Integer))
    reviews = relationship('BillReview', backref='bill')


bill_and_status = select([func.unnest(Bill.status_ids).label('bill_status_id'),
                        Bill.id.label('bill_id')]).alias()


Bill.statuses = relationship("BillStatus",
            secondary=bill_and_status,
            primaryjoin=Bill.id == bill_and_status.c.bill_id,
            secondaryjoin=bill_and_status.c.bill_status_id == BillStatus.id,
            viewonly=True,
            backref='bills')
