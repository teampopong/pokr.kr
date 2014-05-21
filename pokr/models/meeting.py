# -*- coding: utf-8 -*-

from datetime import date

from sqlalchemy import Column, Date, Integer, Text
from sqlalchemy.dialects.postgresql import JSON

from pokr.database import Base


class Meeting(Base):
    __tablename__ = 'meeting'

    # Identifiers
    id = Column(Integer, autoincrement=True, primary_key=True)
    committee_id = Column(Text, index=True)
    parliament = Column(Integer, nullable=False, index=True)
    session = Column(Integer, nullable=False, index=True)
    sitting = Column(Integer, nullable=False, index=True)

    # Meta & contents
    date = Column(Date, nullable=False, index=True)
    content_json = Column(JSON)

