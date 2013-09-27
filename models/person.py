# -*- coding: utf-8 -*-

from sqlalchemy import Column, Date, Enum, func, Integer, Text
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import column_property, deferred, relationship
from sqlalchemy.sql import select

from database import Base
from models import Table
from models.person_image import PersonImage
from utils.hstore import Hstore


class Person(Table, Base):
    __tablename__ = 'person'
    __endpoint__ = 'person'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, index=True)
    name_en = Column(Text, index=True)
    name_cn = Column(Text)

    gender = Column(Enum('m', 'f', name='enum_gender'), index=True)
    birthday = Column(Date, index=True)

    # twitter, facebook, blog, homepage, wiki
    sites = deferred(Column(Hstore, nullable=False, default={}), group='extra')

    ### Joined Properties ###
    profile_image = column_property(select([PersonImage.url])\
                                    .where(PersonImage.person_id == id)\
                                    .order_by(PersonImage.modified_at.desc())\
                                    .limit(1))

    ### Relations ###
    parties = relationship('Party',
            secondary='party_affiliation',
            order_by='desc(party_affiliation.c.start_date)',
            backref='members')

    candidacies = relationship('Candidacy',
            secondary='party_affiliation',
            order_by='desc(Candidacy.election_date)')

    images = relationship('PersonImage',
            order_by='desc(PersonImage.modified_at)',
            backref='person')

    addresses = relationship('NamedRegion',
            secondary='residence',
            order_by='desc(residence.c.id)',
            backref='residents')

    @hybrid_property
    def birthday_year(self):
        return self.birthday.year()

    @birthday_year.expression
    def birthday_year(cls):
        return func.year(cls.birthday)

