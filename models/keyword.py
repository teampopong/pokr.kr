# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, Text

from database import Base
from models import Table


class Keyword(Table, Base):
    __tablename__ = 'keyword'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text, index=True, nullable=False, unique=True)

