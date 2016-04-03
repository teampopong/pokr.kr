# -*- coding: utf-8 -*-

import os
import re

from sqlalchemy import Boolean, Column, Date, func, Integer, select, String, Text, Unicode
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import column_property, relationship
from sqlalchemy.sql.expression import distinct

from pokr.database import Base, db_session
from .bill_keyword import bill_keyword
from .bill_status import BillStatus
from .candidacy import Candidacy
from .cosponsorship import Cosponsorship
from .election import Election
from .party import Party
from .person import Person

from settings import BILLPDF_DIR, BILLTXT_DIR, THIS_ASSEMBLY

numbers_re = re.compile(r'\d+')


class Bill(Base):
    __tablename__ = 'bill'

    id = Column(String(20), primary_key=True)
    name = Column(Unicode(256), index=True, nullable=False)
    summary = Column(Text)

    assembly_id = Column(Integer, index=True, nullable=False)
    proposed_date = Column(Date, index=True)
    decision_date = Column(Date, index=True)

    is_processed = Column(Boolean, index=True)
    link_id = Column(String(40), index=True)
    document_url = Column(Text)

    sponsor = Column(Unicode(80), index=True)
    status_id = Column(Integer, nullable=False)
    status_ids = Column(ARRAY(Integer))
    reviews = relationship('BillReview', backref='bill')

    status = column_property(select([BillStatus.name])\
                             .where(BillStatus.id==status_id), deferred=True)
    keywords = relationship('Keyword',
            secondary=bill_keyword,
            order_by='desc(bill_keyword.c.weight)')

    @property
    def document_pdf_path(self):
        assembly_id = assembly_id_by_bill_id(self.id)
        filepath = '%s/%d/%s.pdf' % (BILLPDF_DIR, assembly_id, self.id)
        if os.path.exists(filepath):
            return filepath
        else:
            return None

    @property
    def document_text_path(self):
        assembly_id = assembly_id_by_bill_id(self.id)
        filepath = '%s/%d/%s.txt' % (BILLTXT_DIR, assembly_id, self.id)
        if os.path.exists(filepath):
            return filepath
        else:
            return None

    @property
    def party_counts(self):
        # if the bill cosponsorships have party_ids, then use it.
        party_counts = db_session.query(func.count(distinct(Cosponsorship.person_id)))\
                                 .join(Cosponsorship.bill)\
                                 .filter(Bill.id == self.id)\
                                 .outerjoin(Cosponsorship.party)\
                                 .add_columns(Party.name, Party.color)\
                                 .group_by(Party.id)

        # Otherwise, use the most recent party affiliation of candidacy info.
        if any(party is None for _, party, _ in party_counts):
            party_counts = db_session.query(Party.name,
                                            func.count(distinct(Person.id)),
                                            Party.color)\
                                     .join(Candidacy)\
                                     .join(Election)\
                                     .filter(Election.assembly_id == self.assembly_id)\
                                     .join(Person)\
                                     .join(Cosponsorship)\
                                     .join(Bill)\
                                     .filter(Bill.id == self.id)\
                                     .group_by(Party.id)
        else:
            party_counts = ((party, count, color)
                            for count, party, color in party_counts)

        return list(party_counts)

    @property
    def representative_people(self):
        return [cosponsor
                for cosponsor in self.cosponsors
                if cosponsor.name in self.sponsor]


bill_and_status = select([func.row_number().over().label('status_order'),
                        func.unnest(Bill.status_ids).label('bill_status_id'),
                        Bill.id.label('bill_id')]).alias()


Bill.statuses = relationship("BillStatus",
            secondary=bill_and_status,
            primaryjoin=Bill.id == bill_and_status.c.bill_id,
            secondaryjoin=bill_and_status.c.bill_status_id == BillStatus.id,
            order_by=bill_and_status.c.status_order,
            viewonly=True,
            backref='bills')


def assembly_id_by_bill_id(bill_id):
    if bill_id.startswith('DD'): # FIXME
        return THIS_ASSEMBLY
    return int(''.join(numbers_re.findall(bill_id))[:2])

