#  -*- coding: utf-8 -*-

from builtins import str
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, UnicodeText

from pokr.database import transaction, Base


class QueryLog(Base):
    __tablename__ = 'query_log'

    id = Column(Integer, autoincrement=True, primary_key=True)
    query = Column(UnicodeText, index=True, nullable=False)
    timestamp = Column(DateTime, index=True, nullable=False)

    def __init__(self, query):
        self.query = query
        self.timestamp = datetime.now()


def log_query(query):
    if not query:
        return
    log = QueryLog(str(query))
    with transaction() as session:
        session.add(log)

