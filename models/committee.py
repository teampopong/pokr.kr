# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship

from database import Base
from models import CascadeForeignKey, Table


class Committee(Table, Base):
    __tablename__ = 'committee'

    id = Column(Integer, autoincrement=True, primary_key=True)
    assembly_id = Column(Integer, CascadeForeignKey('assembly.id'), nullable=False,
            index=True)
    name = Column(Text, nullable=False, index=True)

    assembly = relationship('Assembly', uselist=False)

