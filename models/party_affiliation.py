# -*- coding: utf-8 -*-

from sqlalchemy import Column, Date, Integer, Text
from sqlalchemy.orm import relationship

from database import Base
from models import CascadeForeignKey, Table


class PartyAffiliation(Table, Base):
    __tablename__ = 'party_affiliation'

    ### keys ###
    id = Column(Integer, autoincrement=True, primary_key=True)
    person_id = Column(Integer, CascadeForeignKey('person.id'), nullable=False,
            index=True)
    party_id = Column(Integer, CascadeForeignKey('party.id'), index=True)

    ### additional infos ###
    start_date = Column(Date, index=True)
    end_date = Column(Date, index=True)

    ### Relations ###
    person = relationship('Person', uselist=False)
    party = relationship('Party', uselist=False)


party_affiliation = PartyAffiliation.__table__

