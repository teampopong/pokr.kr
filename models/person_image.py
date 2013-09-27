# -*- coding: utf-8

from sqlalchemy import Column, func, Integer, select, Text
from sqlalchemy.orm import relationship

from database import Base
from models import CascadeForeignKey, Table


class PersonImage(Table, Base):
    __tablename__ = 'person_image'

    id = Column(Integer, autoincrement=True, primary_key=True)
    person_id = Column(Integer, CascadeForeignKey('person.id'), index=True)
    url = Column(Text)

