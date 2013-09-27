# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer

from database import Base
from models import CascadeForeignKey, Table


class Residence(Table, Base):
    __tablename__ = 'residence'

    id = Column(Integer, autoincrement=True, primary_key=True)
    person_id = Column(Integer, CascadeForeignKey('person.id'),
            nullable=False, index=True)
    named_region_id = Column(Integer, CascadeForeignKey('named_region.id'),
            nullable=False, index=True)


residence = Residence.__table__

