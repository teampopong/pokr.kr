from sqlalchemy import CHAR, Column, Integer, String, Unicode
from sqlalchemy.orm import backref, relationship

from pokr.database import Base
from utils.api_model import ApiModel
from .candidacy import Candidacy


class Party(Base, ApiModel):
    __tablename__ = 'party'
    __kind_single__ = 'party'
    __kind_list__ = 'parties'


    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Unicode(20), nullable=False, index=True)
    color = Column(CHAR(6))
    logo = Column(String(1024))

    # derived(duplicated) infos
    order = Column(Integer)
    size = Column(Integer)

    def _to_dict_light(self):
        d = self._columns_to_dict()
        del d['order']
        return d

