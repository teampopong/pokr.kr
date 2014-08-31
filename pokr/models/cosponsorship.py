from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from pokr.database import Base


class Cosponsorship(Base):
    __tablename__ = 'cosponsorship'

    id = Column(Integer, autoincrement=True, primary_key=True)
    person_id = Column(Integer, ForeignKey('person.id'), nullable=False, index=True)
    bill_id = Column(String(20), ForeignKey('bill.id'), nullable=False, index=True)
    party_id = Column(Integer, ForeignKey('party.id'), index=True)
    is_sponsor = Column(Boolean, default=False, index=True)

    bill = relationship('Bill', backref='cosponsorships')
    party = relationship('Party')


cosponsorship = Cosponsorship.__table__

