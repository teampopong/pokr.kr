# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, Integer

from pokr.database import Base


class FavoritePerson(Base):
    __tablename__ = 'favorite_person'

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'),
            nullable=False, index=True)
    person_id = Column(Integer, ForeignKey('person.id', onupdate='CASCADE', ondelete='CASCADE'),
            nullable=False, index=True)

