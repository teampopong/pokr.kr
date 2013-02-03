# -*- coding: utf-8 -*-

from sqlalchemy import CHAR, Column, Enum, Integer
from sqlalchemy.orm import backref, relationship
from database import Base

class Election(Base):
    __tablename__ = 'election'

    id = Column(Integer, autoincrement=True, primary_key=True)
    type = Column(Enum('assembly', 'mayor', 'president', name='enum_election_type'), nullable=False, index=True)
    age = Column(Integer, nullable=False, index=True)
    date = Column(CHAR(8), index=True)

    candidates = relationship('Candidacy',
            primaryjoin='and_(Candidacy.election_id==Election.id)',
            backref=backref('election', lazy=False))
    winners = relationship('Candidacy',
            primaryjoin='and_(Candidacy.election_id==Election.id,'
                             'Candidacy.is_elected==True)')

    def __init__(self, _type, age, date=None):
        self.type = _type
        self.age = age
        if date:
            self.date = date

