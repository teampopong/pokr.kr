# -*- coding: utf-8 -*-

from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, Integer, Text
from popong_models import Base

from utils.enum import DeclEnum


class FeedType(DeclEnum):
    bill = 'B', 'Bill'


class Feed(Base):
    __tablename__ = 'feed'

    id = Column(Integer, autoincrement=True, primary_key=True)
    type = Column(FeedType.db_type())
    created_at = Column(DateTime, default=datetime.now, index=True)

    __mapper_args__ = {
        'polymorphic_on': type,
    }

    def to_html(self):
        raise NotImplementedError()

