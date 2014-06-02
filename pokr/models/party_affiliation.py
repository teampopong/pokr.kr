from sqlalchemy import Column, Date, ForeignKey, Integer
from sqlalchemy.orm import relationship

from pokr.database import Base


__all__ = ['PartyAffiliation']


class PartyAffiliation(Base):
    __tablename__ = 'party_affiliation'

    id = Column(Integer, autoincrement=True, primary_key=True)
    person_id = Column(Integer, ForeignKey('person.id'), nullable=False, index=True)
    party_id = Column(Integer, ForeignKey('party.id'), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)

