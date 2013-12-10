from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, select, String, Unicode
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import column_property
from database import Base

from models.election import Election

class Candidacy(Base):
    __tablename__ = 'candidacy'

    ### join ###
    id = Column(Integer, autoincrement=True, primary_key=True)
    person_id = Column(Integer, ForeignKey('person.id'), nullable=False)
    election_id = Column(Integer, ForeignKey('election.id'), nullable=False)
    party_id = Column(Integer, ForeignKey('party.id'))

    ### additional infos ###
    district = Column(ARRAY(Unicode(20)))
    district_id = Column(ARRAY(String(16)))
    assembly_id = column_property(select([Election.assembly_id])\
                                      .where(Election.id==election_id))
    is_elected = Column(Boolean, default=False, index=True)
    cand_no = Column(Integer)
    vote_score = Column(Integer)
    vote_share = Column(Float)

