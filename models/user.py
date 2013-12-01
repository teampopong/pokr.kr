# -*- coding: utf-8 -*-

from flask.ext.login import UserMixin
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Unicode
from sqlalchemy.orm import relationship

from database import Base

class User(Base, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, autoincrement=True, primary_key=True)
    active = Column(Boolean, default=True)
    email = Column(String(200))
    name = Column(Unicode(40), index=True)
    password = Column(String(200), default='')
    username = Column(String(200))
    address_id = Column(String(16), ForeignKey('region.id', onupdate='CASCADING', ondelete='CASCADING'), index=True)

    address = relationship('Region', uselist=False)
    favorite_keywords = relationship('Keyword',
            secondary='favorite_keyword')
    favorite_people = relationship('Person',
            secondary='favorite_person')

    def is_active(self):
        return self.active

