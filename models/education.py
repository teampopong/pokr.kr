# -*- coding: utf-8

from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship

from database import Base
from models import CascadeForeignKey, Table


class Education(Table, Base):
    __tablename__ = 'education'

    ### keys ###
    id = Column(Integer, autoincrement=True, primary_key=True)
    person_id = Column(Integer, CascadeForeignKey('person.id'), nullable=False,
            index=True)
    school_id = Column(Integer, CascadeForeignKey('school.id'), index=True)

    ### additional infos ###
    description = Column(Text)
    order = Column(Integer, index=True)

    ### Joins ###
    school = relationship('School', uselist=False)


education = Education.__table__

