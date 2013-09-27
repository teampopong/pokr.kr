# -*- coding: utf-8 -*-

from sqlalchemy import Column, event, func, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import and_, bindparam

from conf.regions import REGION_ID_LENGTH
from database import Base
from models import CascadeForeignKey, Table


__all__ = ['Region']


class Region(Table, Base):
    __tablename__ = 'region'
    __endpoint__ = 'region'

    id = Column(Text, primary_key=True)
    parent_id = Column(Text, CascadeForeignKey('region.id'), index=True)

    name = Column(Text, nullable=False, index=True)
    name_en = Column(Text)
    name_cn = Column(Text)

    # memoized
    fullname = Column(Text, index=True)
    fullname_en = Column(Text)

    ### Relations ###
    parent = relationship('Region', remote_side=[id], uselist=False,
            backref='children')

    # is_province, is_municipality, is_submunicipality
    def is_of(self, class_):
        expected =  REGION_ID_LENGTH.get(class_)
        return len(self.id) == expected

    def update_fullname(self):
        regions = list(parents(self)) + [self]
        self.fullname = ' '.join(region.name for region in regions)
        self.fullname_en = ' '.join(region.name_en for region in regions)


def parents(region):
    return Region.query\
                 .filter(and_(
                     bindparam('prefix', region.id).startswith(Region.id),
                     region.id != Region.id))\
                 .order_by(func.length(Region.id))


def update_fullnames_table(mapper, connection, target):
    update_fullnames(target)


def update_fullnames_attr(target, value, oldvalue, initiator):
    update_fullnames(target)


def update_fullnames(region):
    successors = Region.query\
                       .filter(Region.id.startswith(region.id))
    for successor in successors:
        successor.update_fullname()


event.listen(Region, 'after_insert', update_fullnames_table)
event.listen(Region, 'after_delete', update_fullnames_table)
event.listen(Region.name, 'set', update_fullnames_attr)

