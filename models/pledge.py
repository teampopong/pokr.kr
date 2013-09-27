# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import backref, relationship

from database import Base
from models import CascadeForeignKey, Table

class Pledge(Table, Base):
    __tablename__ = 'pledge'

    id = Column(Integer, autoincrement=True, primary_key=True)
    candidacy_id = Column(Integer, CascadeForeignKey('candidacy.id'),
                          nullable=False, index=True)
    no = Column(Integer, nullable=False, index=True)
    title = Column(Text)
    description = Column(Text)

    ### Relations ###
    candidacy = relationship('Candidacy', uselist=False,
                             backref=backref('pledges', order_by='Pledge.no'))

