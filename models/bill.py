# -*- coding: utf-8 -*-

from sqlalchemy import Column, Date, Integer, String, Unicode
from database import Base

class Bill(Base):
    __tablename__ = 'bill'

    # TODO: 대수 입력
    # TODO: `proposers` join
    # TODO: Convert `status`, `proposer_type` to Enum

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Unicode(150))

    proposed_date = Column(Date)
    decision_date = Column(Date)

    committee = Column(Unicode(30), nullable=True)
    proposer_type = Column(Integer)

    status = Column(Integer, index=True)
    status_detail = Column(Unicode(10))
    link_id = Column(String(40), index=True)
