# -*- encoding: utf-8 -*-

from datetime import date
import json

from flaskext.babel import format_date
from sqlalchemy import CHAR, Column, Enum, func, Integer, String, Text, Unicode
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import backref, deferred, relationship
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.sql.expression import and_, desc

from api.model import ApiModel
from pokr.database import Base
from .bill_withdrawal import bill_withdrawal
from .candidacy import Candidacy
from .cosponsorship import cosponsorship
from .party import Party


class Person(Base, ApiModel):
    __tablename__ = 'person'
    __kind_single__ = 'person'
    __kind_list__ = 'people'

    id = Column(Integer, primary_key=True)

    ### Fields ###
    name = Column(Unicode(20), nullable=False, index=True)
    name_en = Column(String(80), index=True)
    name_cn = Column(Unicode(20), index=True)

    gender = Column(Enum('m', 'f', name='enum_gender'), index=True)

    birthday = Column(CHAR(8), index=True)

    education = deferred(Column(ARRAY(Unicode(60))), group='profile')
    education_id = deferred(Column(ARRAY(String(20))), group='profile')

    address = deferred(Column(ARRAY(Unicode(20))), group='profile')
    address_id = deferred(Column(ARRAY(String(16))), group='profile')

    image = Column(String(1024))
    twitter = deferred(Column(String(20)), group='extra')
    facebook = deferred(Column(String(80)), group='extra')
    blog = deferred(Column(String(255)), group='extra')
    homepage = deferred(Column(String(255)), group='extra')
    wiki = deferred(Column(Text), group='extra')
    extra_vars = deferred(Column(Text), group='extra')

    ### Relations ###
    candidacies = relationship('Candidacy',
            order_by='desc(Candidacy.assembly_id)',
            backref='person')
    bills_ = relationship('Bill',
            secondary=cosponsorship,
            order_by='desc(Bill.proposed_date)',
            backref='cosponsors')
    withdrawed_bills = relationship('Bill',
            secondary=bill_withdrawal,
            backref='withdrawers')

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
    def parties(self):
        # FIXME: relationship w/ party_affiliation
        parties = Party.query.join(Candidacy,
                                  Candidacy.party_id == Party.id)\
                            .join(Person,
                                  Person.id == Candidacy.person_id)\
                            .filter(Person.id == self.id)\
                            .order_by(desc(Candidacy.assembly_id))
        return parties

    @property
    def cur_party(self):
        return self.parties.first()

    def _to_dict_light(self):
        d = self._columns_to_dict()
        extra_vars = json.loads(self.extra_vars)

        del d['extra_vars']
        d['address'] = extra_vars.get('address')
        d['education'] = extra_vars.get('education')
        d['birthday'] = self.birthday_date.isoformat()
        # TODO: add relation data
        return d


def guess_person(session, name, assembly_id):
    name = name.split('(')[0]
    try:
        person = session.query(Person)\
                        .filter_by(name=name)\
                        .join(Person.candidacies)\
                        .filter(Candidacy.assembly_id == assembly_id)\
                        .one()

    except MultipleResultsFound, e:
        person = session.query(Person)\
                        .filter_by(name=name)\
                        .join(Person.candidacies)\
                        .filter(and_(Candidacy.assembly_id == assembly_id,
                                     Candidacy.is_elected == True))\
                        .one()
    return person

