from sqlalchemy import CHAR, Boolean, Column, ForeignKey, Integer
from models.base import Base

class PartyAffiliation(Base):
    __tablename__ = 'party_affiliation'

    ### join ###
    id = Column(Integer, autoincrement=True, primary_key=True)
    person_id = Column(Integer, ForeignKey('person.id'))
    party_id = Column(Integer, ForeignKey('party.id'))

    ### additional infos ###
    start_date = Column(CHAR(8))
    end_date = Column(CHAR(8))
    is_current_member = Column(Boolean, default=True, index=True)

