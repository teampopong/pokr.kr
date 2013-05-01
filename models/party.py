from sqlalchemy import CHAR, Column, Integer, Unicode
from sqlalchemy.orm import backref, relationship
from database import Base
from models.party_affiliation import party_affiliation

class Party(Base):
    __tablename__ = 'party'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Unicode(20), nullable=False, index=True)
    color = Column(CHAR(6))

    members = relationship('Person',
            secondary=party_affiliation,
            backref='party')

    def __init__(self, name, color=None):
        self.name = name
        if color:
            self.color = color
