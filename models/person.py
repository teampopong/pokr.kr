# -*- encoding: utf-8 -*-

from sqlalchemy import CHAR, Column, Enum, Integer, Unicode
from sqlalchemy.orm import backref, relationship
from models.base import Base

class Person(Base):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)

    ### Fields ###
    name = Column(Unicode(20), nullable=False, index=True)
    name_cn = Column(Unicode(20))

    gender = Column(Enum('m', 'f', name='enum_gender'), index=True)

    birthday = Column(CHAR(8), index=True)

    birth_city = Column(Unicode(20), index=True)
    birth_county = Column(Unicode(20))

    addr_city = Column(Unicode(20))
    addr_county = Column(Unicode(20))
    addr_detail = Column(Unicode(80))

    ### Relations ###
    affiliations = relationship('PartyAffiliation',
            order_by='PartyAffiliation.end_date',
            backref=backref('person', lazy=False))
    educations = relationship('Education',
            order_by='Education.start_year',
            backref=backref('person', lazy=False))
    elections = relationship('Candidacy',
            order_by='Candidacy.election.date',
            backref=backref('person', lazy=False))
    experiences = relationship('Experience',
            order_by='Experience.enddate',
            backref=backref('person', lazy=False))

