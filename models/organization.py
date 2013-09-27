# -*- coding: utf-8 -*-

from sqlalchemy import Column, Date, Integer, Text
from sqlalchemy.orm import column_property, relationship
from sqlalchemy.sql import select

from database import Base
from models import CascadeForeignKey, Table
from models.organization_type import OrganizationType


class Organization(Table, Base):
    __tablename__ = 'organization'

    id = Column(Integer, autoincrement=True, primary_key=True)
    type_id = Column(Integer, CascadeForeignKey('organization_type.id'),
            nullable=False, index=True)

    ### additional infos ###
    name = Column(Text, nullable=False, index=True)
    start_date = Column(Date, index=True)
    end_date = Column(Date, index=True)

    ### Joined Properties ###
    type_name = column_property(select([OrganizationType.name])\
                                .where(OrganizationType.id==type_id))

    __mapper_args__ = {
        'polymorphic_on': type_name,
        'polymorphic_identity': 'organization'
    }

    ### Relations ###
    type = relationship('OrganizationType', uselist=False, backref='organizations')

