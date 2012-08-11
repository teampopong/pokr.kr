# -*- encoding: utf-8 -*-

from sqlalchemy import Column, Enum, Integer, Unicode
from sqlalchemy.orm import backref, column_property, relationship
from models.base import Base

class Person(Base):
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True)

    ### Names ###
    name = Column(Unicode(20), index=True, nullable=False)
    name_cn = Column(Unicode(20))

    ### basic infos ###
    sex = Column(Enum('m', 'f', name='enum_sex'), index=True)

    ### Birth ###
    birthyear = Column(Integer)
    birthmonth = Column(Integer)
    birthday = Column(Integer)
    # TODO: birthdate

    birthcity = Column(Unicode(20))
    addresss = Column(Unicode(160))

    ### Relations ###
    affiliations = relationship('PersonParty',
            order_by='PersonParty.end_date',
            backref=backref('person', lazy=False))
    educations = relationship('PersonSchool',
            order_by='PersonSchool.adm_year',
            backref=backref('person', lazy=False))
    elections = relationship('PersonElection',
            order_by='PersonElection.election.date',
            backref=backref('person', lazy=False))
    experiences = relationship('Job',
            order_by='Job.enddate',
            backref=backref('person', lazy=False))

