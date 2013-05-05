from sqlalchemy import Column, Integer, Unicode
from sqlalchemy.orm import backref, relationship
from database import Base
from models.person import Person

class School(Base):
    __tablename__ = 'school'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Unicode(40))

    @property
    def alumni(self):
        return Person.query.filter(Person.education_id.any(str(self.id))).all()

