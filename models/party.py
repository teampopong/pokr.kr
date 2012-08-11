from sqlalchemy import CHAR, Column, Integer, Unicode
from sqlalchemy.orm import backref, relationship
from models.base import Base

class Party(Base):
    __tablename__ = 'parties'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Unicode(20), nullable=False)
    color = Column(CHAR(6))

    members = relationship('PersonParty', backref=backref('party', lazy=False))
