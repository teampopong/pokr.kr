from flask.ext.login import UserMixin
from sqlalchemy import Boolean, Column, Integer, String, Unicode

from database import Base

class User(Base, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, autoincrement=True, primary_key=True)
    active = Column(Boolean, default=True)
    email = Column(String(200))
    name = Column(Unicode(40), index=True)
    password = Column(String(200), default='')
    username = Column(String(200))

