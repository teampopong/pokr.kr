from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, select, Unicode
from sqlalchemy.orm import column_property
from models.base import Base

class Candidacy(Base):
    __tablename__ = 'candidacy'

    ### join ###
    id = Column(Integer, autoincrement=True, primary_key=True)
    person_id = Column(Integer, ForeignKey('person.id'), nullable=False)
    election_id = Column(Integer, ForeignKey('election.id'), nullable=False)
    party_id = Column(Integer, ForeignKey('party.id'))

    ### additional infos ###
    region1 = Column(Unicode(20), nullable=False, index=True)
    region2 = Column(Unicode(20), index=True)
    region3 = Column(Unicode(4), index=True)
    is_elected = Column(Boolean, default=False, index=True)
    cand_no = Column(Integer)
    vote_score = Column(Integer)
    vote_rate = Column(Float)
    party = column_property(
        select(['Party.name']).where('Party.id==party_id')
    )

