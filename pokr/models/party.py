from sqlalchemy import CHAR, Column, Integer, String, Unicode
from sqlalchemy.orm import backref, relationship

from pokr.database import Base
from .candidacy import Candidacy


class Party(Base):
    __tablename__ = 'party'


    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Unicode(20), nullable=False, index=True)
    color = Column(CHAR(6))
    logo = Column(String(1024))

    # derived(duplicated) infos
    order = Column(Integer)
    size = Column(Integer)

