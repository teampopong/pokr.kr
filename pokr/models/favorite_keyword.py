# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, Integer

from pokr.database import Base


class FavoriteKeyword(Base):
    __tablename__ = 'favorite_keyword'

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'),
            nullable=False, index=True)
    keyword_id = Column(Integer, ForeignKey('keyword.id', onupdate='CASCADE', ondelete='CASCADE'),
            nullable=False, index=True)

