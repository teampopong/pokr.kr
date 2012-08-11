# -*- coding: utf-8 -*-

from sqlalchemy import Column, Date, Enum, Integer
from sqlalchemy.orm import backref, relationship
from models.base import Base

class Election(Base):
    __tablename__ = 'elections'

    id = Column(Integer, primary_key=True)
    type = Column(Enum('assembly', 'mayor', 'president', name='enum_election_type'), nullable=False)
    nth = Column(Integer, nullable=False)
    date = Column(Date)

    candidates = relationship('PersonElection',
            primaryjoin='and_(PersonElection.election_id==Election.id)',
            backref=backref('election', lazy=False))
    winners = relationship('PersonElection',
            primaryjoin='and_(PersonElection.election_id==Election.id,'
                             'PersonElection.is_electied==True)')


