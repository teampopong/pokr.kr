# -*- coding: utf-8 -*-

import json
from collections import defaultdict

from sqlalchemy import Boolean, Column, Date, Integer, Text
from sqlalchemy.orm import backref, column_property, relationship
from sqlalchemy.sql import select

from database import Base
from models import CascadeForeignKey, Table
from models.bill_status import BillStatus
from models.bill_process import BillProcess
from utils.hstore import Hstore


class Bill(Table, Base):
    __tablename__ = 'bill'

    id = Column(Text, primary_key=True)
    link_id = Column(Text, index=True)
    assembly_id = Column(Integer, CascadeForeignKey('assembly.id'), nullable=False,
            index=True)

    ### additional infos ###
    name = Column(Text, nullable=False, index=True)
    summary = Column(Text)
    document_url = Column(Text)
    proposed_date = Column(Date, index=True)
    decision_date = Column(Date, index=True)
    is_processed = Column(Boolean, index=True)  # TODO: how to update?
    extra_vars = Column(Hstore, nullable=False, default={})

    ### Joined Properties ###
    status = column_property(select([BillStatus.name],
                                     BillStatus.id == BillProcess.status_id)\
                             .where(BillProcess.bill_id==id)\
                             .order_by(BillProcess.order.desc()))

    ### Relations ###
    assembly = relationship('Assembly', uselist=False)
    keywords = relationship('Keyword',
            secondary='bill_keyword',
            order_by='desc(bill_keyword.c.weight)',
            backref='bills')
    statuses = relationship('BillStatus',
            secondary='bill_process',
            order_by='bill_process.c.order')
    cosponsorships = relationship('Cosponsorship',
            backref=backref('bill', uselist=False))

    ### Methods ###
    @property
    def party_counts(self):
        dump = extra_vars.get('party_counts')
        party_counts = json.load(dump) if dump else {}
        return party_counts

    def update_statistics(self):
        party_counts = defaultdict(int)
        for cosponsorship in self.cosponsorships:
            party = Cosponsorship.party
            party_name = party.name if party else 'unknown'
            party_counts[party_name] += 1
        extra_vars['party_counts'] = json.dump(dict(party_counts))


def assembly_id_by_bill_id(bill_id):
    return int(bill_id.lstrip('Z')[:2])

