from sqlalchemy import Column, Integer, Unicode
from sqlalchemy.orm import backref, relationship
from database import Base
from models.education import education

class School(Base):
    __tablename__ = 'school'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Unicode(40))
    alumnis = relationship('Person',
            secondary=education,
            backref='school')

