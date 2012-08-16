from sqlalchemy import CHAR, Column, Integer, Unicode
from sqlalchemy.orm import backref, relationship
from models.base import Base

class Party(Base):
    __tablename__ = 'party'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Unicode(20), nullable=False, index=True)
    color = Column(CHAR(6))

    members = relationship('PartyAffiliation', backref=backref('party', lazy=False))
