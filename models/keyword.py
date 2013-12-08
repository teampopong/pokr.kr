# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, Text, UnicodeText

from database import Base


class Keyword(Base):
    __tablename__ = 'keyword'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(UnicodeText, index=True, nullable=False)
    image = Column(Text)

    def __init__(self, name):
        self.name = name

