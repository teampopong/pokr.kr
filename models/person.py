# -*- encoding: utf-8 -*-

from collections import defaultdict
from datetime import date

from flaskext.babel import format_date
from sqlalchemy import CHAR, Column, Enum, func, Integer, String, Text, Unicode
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import backref, relationship

from database import Base
from models.candidacy import Candidacy
from models.party_affiliation import party_affiliation
from models.pledge import Pledge

class Person(Base):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)

    ### Fields ###
    name = Column(Unicode(20), nullable=False, index=True)
    name_en = Column(String(80), index=True)
    name_cn = Column(Unicode(20), index=True)

    gender = Column(Enum('m', 'f', name='enum_gender'), index=True)

    birthday = Column(CHAR(8), index=True)

    birth_city = Column(Unicode(20), index=True)
    birth_county = Column(Unicode(20), index=True)

    education = Column(ARRAY(Unicode(60)))
    education_id = Column(ARRAY(String(20)))

    address = Column(ARRAY(Unicode(20)))
    address_id = Column(ARRAY(String(16)))

    image = Column(String(1024))
    twitter = Column(String(20))
    facebook = Column(String(80))
    blog = Column(String(255))
    homepage = Column(String(255))
    extra_vars = Column(Text)

    ### Relations ###
    parties = relationship('Party',
            secondary=party_affiliation,
            order_by=party_affiliation.columns['start_date'].desc(),
            backref='person')
    candidacies = relationship('Candidacy',
            order_by='desc(Candidacy.age)',
            backref='person')
    experiences = relationship('Experience',
            order_by='Experience.end_date',
            backref=backref('person'))

    def __init__(self, name, **kwargs):
        self.name = name

        for key, val in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

    @hybrid_property
    def birthday_year(self):
        return int(self.birthday[:4])

    @birthday_year.expression
    def birthday_year(cls):
        return func.substr(cls.birthday, 1, 4)

    @property
    def birthday_month(self):
        return int(self.birthday[4:6]) or 1

    @property
    def birthday_day(self):
        return int(self.birthday[6:8]) or 1

    @property
    def birthday_date(self):
        return date(self.birthday_year,
                self.birthday_month,
                self.birthday_day)

    @property
    def birthday_formatted(self):
        return format_date(self.birthday_date)

    @property
    def cur_party(self):
        return self.parties[0] if self.parties else None

    @property
    def pledges(self):
        query = Pledge.query.join(Candidacy,
                                  Candidacy.id == Pledge.candidacy_id)\
                            .join(Person,
                                  Person.id == Candidacy.person_id)\
                            .filter(Person.id == self.id)\
                            .order_by(Pledge.id)

        result = defaultdict(list)
        for pledge in query:
            result[pledge.candidacy.age].append(pledge)

        return result

