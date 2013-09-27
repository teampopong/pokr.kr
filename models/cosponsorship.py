# -*- coding: utf-8 -*-

from sqlalchemy import Boolean, Column, event, Integer, Text
from sqlalchemy.orm import relationship

from database import Base
from models import CascadeForeignKey, Table


class Cosponsorship(Table, Base):
    __tablename__ = 'cosponsorship'

    id = Column(Integer, autoincrement=True, primary_key=True)
    bill_id = Column(Text, CascadeForeignKey('bill.id'), nullable=False,
            index=True)
    name = Column(Text, nullable=False, index=True)
    committee_id = Column(Integer, CascadeForeignKey('committee.id'),
            index=True)
    party_affiliation_id = Column(Integer, CascadeForeignKey('party_affiliation.id'),
            index=True)

    # 대표발의
    is_proposer = Column(Boolean, default=False, nullable=False, index=True)
    # 찬성발의
    is_agreement = Column(Boolean, default=False, nullable=False, index=True)
    # 철회
    is_withdrawn = Column(Boolean, default=False, nullable=False, index=True)

    ### Relations ###
    party = relationship('Party',
            secondary='party_affiliation',
            uselist=False)
    person = relationship('Person',
            secondary='party_affiliation',
            uselist=False)


cosponsorship = Cosponsorship.__table__


def update_bill_statistics(mapper, connection, target):
    target.bill.update_statistics()


event.listen(Cosponsorship, 'after_insert', update_bill_statistics)
event.listen(Cosponsorship, 'after_delete', update_bill_statistics)

