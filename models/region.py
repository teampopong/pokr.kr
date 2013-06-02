from sqlalchemy import Column, String, Unicode
from sqlalchemy.sql.expression import bindparam
from database import Base

from database import db_session
from models.person import Person
from models.election import Election
from models.candidacy import Candidacy

class Region(Base):
    __tablename__ = 'region'

    id = Column(String(16), primary_key=True)
    name = Column(Unicode(20), index=True, nullable=False)
    name_cn = Column(Unicode(20))
    name_en = Column(String(80))

    @property
    def officials(self):
        officials_ = db_session.query(Person.id, Candidacy.age)\
                     .filter(Candidacy.person_id == Person.id)\
                     .filter(Candidacy.district_id.any(self.id))\
                     .filter(Candidacy.is_elected == True)\
                     .group_by(Person.id, Candidacy.election_id)
        return { o[1]: o[0] for o in officials_ }

    @property
    def candidates(self):
        return Person.query\
                     .join(Candidacy)\
                     .filter(Candidacy.person_id == Person.id)\
                     .filter(Candidacy.district_id.any(self.id))\
                     .group_by(Person.id)

    @property
    def residents(self):
        return Person.query\
                     .filter(Person.address_id.any(self.id))\
                     .group_by(Person.id)

    @property
    def fullname(self):
        fullname = ' '.join(region.name for region in self.parents)
        return fullname

    @property
    def fullname_en(self):
        regions = self.parents
        fullname = ' '.join(region.name_en for region in self.parents)
        return fullname

    @property
    def parents(self):
        return Region.query\
                     .filter(bindparam('prefix', self.id).startswith(Region.id))\
                     .order_by(Region.id)
