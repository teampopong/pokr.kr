# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, Integer

from pokr.database import Base


class FavoriteBill(Base):
    __tablename__ = 'favorite_bill'

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'),
            nullable=False, index=True)
    bill_id = Column(Integer, ForeignKey('bill.id', onupdate='CASCADE', ondelete='CASCADE'),
            nullable=False, index=True)
