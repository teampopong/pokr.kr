# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, UnicodeText

from database import Base


class Keyword(Base):
    __tablename__ = 'keyword'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(UnicodeText, index=True, nullable=False)

