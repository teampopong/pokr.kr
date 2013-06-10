from sqlalchemy import CHAR, Column, Integer, String, Unicode
from sqlalchemy.orm import backref, relationship

from database import Base
from models.candidacy import Candidacy

class Party(Base):
    __tablename__ = 'party'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Unicode(20), nullable=False, index=True)
    color = Column(CHAR(6))
    logo = Column(String(1024))

    # derived(duplicated) infos
    order = Column(Integer)
    size = Column(Integer)

    def __init__(self, name, color=None):
        self.name = name
        if color:
            self.color = color

    @property
    def members(self):
        if 'Person' not in dir():
            from models.person import Person
        return Person.query.join(Candidacy,
                                 Person.id == Candidacy.person_id)\
                           .join(Party,
                                 Party.id == Candidacy.party_id)\
                           .filter(Party.id == self.id)\
                           .group_by(Person.id)
