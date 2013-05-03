# -*- coding: utf-8 -*-

from sqlalchemy import Column, Date, Integer, String, Unicode
from sqlalchemy.dialects.postgresql import ARRAY
from database import Base


class Bill(Base):
    __tablename__ = 'bill'

    id = Column(String(20), primary_key=True)
    name = Column(Unicode(150), nullable=False)

    age = Column(Integer, index=True, nullable=False)
    proposed_date = Column(Date, index=True)
    decision_date = Column(Date, index=True)

    proposers = Column(ARRAY(Unicode(100)))
    proposer_representative = Column(Unicode(100))
    committee = Column(Unicode(100), index=True)
    proposer_type = Column(Integer, index=True)

    status = Column(Integer, index=True)
    status_detail = Column(Unicode(10))
    link_id = Column(String(40), index=True)
    attachments = Column(ARRAY(String(1024)))
