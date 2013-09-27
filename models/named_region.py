# -*- coding: utf-8

from sqlalchemy import Column, Integer, Text

from database import Base
from models import CascadeForeignKey, Table

class NamedRegion(Table, Base):
    __tablename__ = 'named_region'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text, nullable=False, index=True)
    region_id = Column(Text, CascadeForeignKey('region.id'), index=True)

