# -*- coding: utf-8 -*-

from sqlalchemy import Boolean, CHAR, Column, Enum, Integer
from sqlalchemy.orm import backref, relationship

from pokr.database import Base


class Election(Base):
    __tablename__ = 'election'

    id = Column(Integer, autoincrement=True, primary_key=True)
    type = Column(Enum('assembly', 'mayor', 'president', name='enum_election_type'), nullable=False, index=True)
    assembly_id = Column(Integer, nullable=False, index=True)
    date = Column(CHAR(8), index=True)
    is_regular = Column(Boolean, default=True, index=True)

    candidates = relationship('Candidacy', backref='election')


def current_parliament_id(type):
    latest_election = Election.query\
                              .filter_by(type=type)\
                              .order_by(Election.assembly_id.desc())\
                              .first()
    if latest_election:
        return latest_election.assembly_id

