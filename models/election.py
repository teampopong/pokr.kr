# -*- coding: utf-8 -*-

from sqlalchemy import Column, Date, Integer
from sqlalchemy.orm import backref, relationship

from database import Base
from models import CascadeForeignKey, Table


class Election(Table, Base):
    __tablename__ = 'election'

    id = Column(Integer, autoincrement=True, primary_key=True)
    organization_id = Column(Integer, CascadeForeignKey('organization.id'),
            index=True)
    date = Column(Date, index=True)

    candidates = relationship('Candidacy',
            backref=backref('election', uselist=False))

    organization = relationship('Organization', uselist=False)

