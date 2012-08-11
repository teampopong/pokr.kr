# -*- coding: utf-8 -*-

from sqlalchemy import Column, Enum, ForeignKey, Integer, Unicode
from models.base import Base

class PersonSchool(Base):
    __tablename__ = 'people_schools'

    ### join ###
    person_id = Column(Integer, ForeignKey('people.id'), primary_key=True)
    school_id = Column(Integer, ForeignKey('schools.id'), primary_key=True)

    ### additional infos ###
    course = Column(Enum('elementary', 'middle', 'high', 'undergrad', 'grad', name='enum_education_course'),
                   index=True)
    mayor = Column(Unicode(20))
    adm_year = Column(Integer, index=True)
    grad_year = Column(Integer)
    status = Column(Enum('a', 'b', 'c', 'd', name='enum_education_status')) # '재학', '중퇴', '졸업', '수료'
