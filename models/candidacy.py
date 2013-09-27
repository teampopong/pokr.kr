# -*- coding: utf-8 -*-

from sqlalchemy import Boolean, Column, Date, Float, Integer, select
from sqlalchemy.orm import column_property, relationship

from database import Base
from models import CascadeForeignKey, Table
from models.election import Election


class Candidacy(Table, Base):
    __tablename__ = 'candidacy'
### keys ###
    id = Column(Integer, autoincrement=True, primary_key=True)
    election_id = Column(Integer, CascadeForeignKey('election.id'),
            nullable=False, index=True, unique='uix_candidacy_1')
    party_affiliation_id = Column(Integer, CascadeForeignKey('party_affiliation.id'),
            nullable=False, index=True, unique='uix_candidacy_1')
    named_region_id = Column(Integer, CascadeForeignKey('named_region.id'),
            index=True)

    ### additional infos ###
    is_elected = Column(Boolean, default=False, index=True)
    cand_no = Column(Integer)
    vote_score = Column(Integer)
    vote_share = Column(Float)

    ### Joined Properties ###
    election_date = column_property(select([Election.date])\
                                        .where(Election.id == election_id))

    ### Relations ###
    party = relationship('Party',
            secondary='party_affiliation',
            backref='candidacies',
            uselist=False)
    person = relationship('Person',
            secondary='party_affiliation',
            uselist=False)
    named_region = relationship('NamedRegion', uselist=False)


candidacy = Candidacy.__table__

