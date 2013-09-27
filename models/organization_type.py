# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, Text

from database import Base
from models import Table


class OrganizationType(Table, Base):
    __tablename__ = 'organization_type'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text, index=True)

