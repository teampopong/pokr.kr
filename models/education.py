# -*- coding: utf-8 -*-

from sqlalchemy import Column, Enum, ForeignKey, Integer, Unicode
from models.base import Base

class Education(Base):
    __tablename__ = 'education'

    ### join ###
    id = Column(Integer, autoincrement=True, primary_key=True)
    person_id = Column(Integer, ForeignKey('person.id'), nullable=False)
    school_id = Column(Integer, ForeignKey('school.id'), nullable=False)

    ### additional infos ###
    course = Column(Enum('elementary', 'middle', 'high', 'undergrad', 'grad',
                         name='enum_education_course'),
                    index=True)
    mayor = Column(Unicode(20))
    start_year = Column(Integer, index=True)
    end_year = Column(Integer)
    status = Column(Enum('in', 'dropped', 'graduated', 'completed',
                    name='enum_education_status'))
