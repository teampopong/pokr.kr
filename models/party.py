from sqlalchemy import CHAR, Column, Integer, String, Unicode
from sqlalchemy.orm import backref, relationship

from api import ApiModel
from database import Base
from models.candidacy import Candidacy

class Party(Base, ApiModel):
    __tablename__ = 'party'
    __kind_single__ = 'party'
    __kind_list__ = 'parties'


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

    def _to_dict_light(self):
        d = self._columns_to_dict()
        del d['order']
        return d

