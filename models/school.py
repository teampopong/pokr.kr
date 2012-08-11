from sqlalchemy import Column, Integer, Unicode
from sqlalchemy.orm import backref, relationship
from models.base import Base

class School(Base):
    __tablename__ = 'schools'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Unicode(40))
    alumnis = relationship('PersonSchool', backref=backref('school', lazy=False))

