# -*- encoding: utf-8 -*-

from collections import defaultdict
from datetime import date
import json

from flaskext.babel import format_date
from sqlalchemy import CHAR, Column, Enum, func, Integer, String, Text, Unicode
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.expression import desc

from api import ApiModel
from database import Base
from models.bill_withdrawal import bill_withdrawal
from models.candidacy import Candidacy
from models.cosponsorship import cosponsorship
from models.party import Party
from models.pledge import Pledge

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

    education = Column(ARRAY(Unicode(60)))
    education_id = Column(ARRAY(String(20)))

    address = Column(ARRAY(Unicode(20)))
    address_id = Column(ARRAY(String(16)))

    image = Column(String(1024))
    twitter = Column(String(20))
    facebook = Column(String(80))
    blog = Column(String(255))
    homepage = Column(String(255))
    extra_vars = deferred(Column(Text)) # TODO: undefer

    ### Relations ###
    candidacies = relationship('Candidacy',
            order_by='desc(Candidacy.age)',
            backref='person')
    bills_ = relationship('Bill',
            secondary=cosponsorship,
            order_by='desc(Bill.proposed_date)',
            backref='cosponsors')
    withdrawed_bills = relationship('Bill',
            secondary=bill_withdrawal,
            backref='withdrawers')

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
    def parties(self):
        parties = Party.query.join(Candidacy,
                                  Candidacy.party_id == Party.id)\
                            .join(Person,
                                  Person.id == Candidacy.person_id)\
                            .filter(Person.id == self.id)\
                            .order_by(desc(Candidacy.age))
        return parties

    @property
    def cur_party(self):
        return self.parties.first()

    @property
    def party_history(self):
        parties_and_ages = self.parties.add_columns(Candidacy.age)
        result = []
        prev_party_id = None
        for party, age in parties_and_ages:
            if prev_party_id == party.id:
                result[-1][0].append(age)
            else:
                result.append(([age], party))
                prev_party_id = party.id
        return [(party, min(ages), max(ages)) for ages, party in result]

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

    def bills(self, age=None):
        if 'Bill' not in dir():
            from models.bill import Bill
        query = Bill.query.join(cosponsorship,
                                Bill.id == cosponsorship.c.bill_id)\
                          .join(Person,
                                Person.id == cosponsorship.c.person_id)\
                          .filter_by(id=self.id)\
                          .order_by(desc(Bill.proposed_date))
        if age:
            query = query.filter(Bill.age == age)

        return query

    def _to_dict_light(self):
        d = self._columns_to_dict()
        extra_vars = json.loads(self.extra_vars)

        del d['extra_vars']
        d['address'] = extra_vars.get('address')
        d['education'] = extra_vars.get('education')
        d['birthday'] = self.birthday_date.isoformat()
        # TODO: add relation data
        return d
