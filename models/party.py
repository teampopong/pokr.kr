from sqlalchemy import CHAR, Column, Integer, Unicode
from sqlalchemy.orm import backref, relationship
from database import Base

class Party(Base):
    __tablename__ = 'party'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Unicode(20), nullable=False, index=True)
    color = Column(CHAR(6))

    members = relationship('PartyAffiliation', backref=backref('party', lazy=False))

    def __init__(self, name, color=None):
        self.name = name
        if color:
            self.color = color
