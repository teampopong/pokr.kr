# -*- coding: utf-8 -*-

from sqlalchemy import Boolean, CHAR, Column, Enum, Integer
from sqlalchemy.orm import backref, relationship
from database import Base

class Election(Base):
    __tablename__ = 'election'

    id = Column(Integer, autoincrement=True, primary_key=True)
    type = Column(Enum('assembly', 'mayor', 'president', name='enum_election_type'), nullable=False, index=True)
    age = Column(Integer, nullable=False, index=True)
    date = Column(CHAR(8), index=True)
    is_regular = Column(Boolean, default=True, index=True)

    candidates = relationship('Candidacy', backref='election')

    def __init__(self, _type, age, date=None, is_regular=None):
        self.type = _type
        self.age = age
        if date:
            self.date = date
        if is_regular:
            self.is_regular = is_regular

