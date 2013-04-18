from sqlalchemy import CHAR, Column, Integer, Unicode
from sqlalchemy.orm import backref, relationship
from database import Base
from models.person import Person
from models.party_affiliation import party_affiliation

class Party(Base):
    __tablename__ = 'party'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Unicode(20), nullable=False, index=True)
    color = Column(CHAR(6))
    order = Column(Integer)

    members = relationship('Person',
            secondary=party_affiliation,
            backref='party')

    def __init__(self, name, color=None):
        self.name = name
        if color:
            self.color = color

    @property
    def current_members(self):
        return Person.query.join(party_affiliation,
                                 Person.id == party_affiliation.c.person_id)\
                           .filter(party_affiliation.c.is_current_member == True)\
                           .join(Party,
                                 Party.id == party_affiliation.c.party_id)\
                           .filter(Party.id == self.id)
