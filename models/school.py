# -*- coding: utf-8

from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship

from database import Base
from models import Table


class School(Table, Base):
    __tablename__ = 'school'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text, nullable=False, index=True)

    ### Relations ###
    alumnis = relationship('Person', secondary='education')

