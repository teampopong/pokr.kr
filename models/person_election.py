from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, select, Unicode
from sqlalchemy.orm import column_property
from models.base import Base

class PersonElection(Base):
    __tablename__ = 'people_elections'

    ### join ###
    person_id = Column(Integer, ForeignKey('people.id'), primary_key=True)
    election_id = Column(Integer, ForeignKey('elections.id'), primary_key=True)
    party_id = Column(Integer, ForeignKey('parties.id'))

    ### additional infos ###
    region = Column(Unicode(20), nullable=False)
    subregion = Column(Unicode(20))
    subsubregion = Column(Unicode(4))
    is_elected = Column(Boolean, default=False)
    cand_no = Column(Integer)
    votenum = Column(Integer)
    voterate = Column(Float)
    party = column_property(
        select(['Party.name']).where('Party.id==party_id')
    )

