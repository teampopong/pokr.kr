from sqlalchemy import Column, String, Unicode
from database import Base

from models.person import Person
from models.candidacy import Candidacy

class Region(Base):
    __tablename__ = 'region'

    id = Column(String(16), primary_key=True)
    name = Column(Unicode(20), index=True, nullable=False)
    name_cn = Column(Unicode(20))
    name_en = Column(String(80))

    @property
    def candidates(self):
        return Person.query\
                     .join(Candidacy)\
                     .filter(Candidacy.person_id == Person.id)\
                     .filter(Candidacy.district_id.any(self.id))

    @property
    def residents(self):
        return Person.query\
                     .filter(Person.address_id.any(self.id))
