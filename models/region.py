from sqlalchemy import Column, String, Unicode
from database import Base

class Region(Base):
    __tablename__ = 'region'

    id = Column(String(16), primary_key=True)
    name = Column(Unicode(20), nullable=False)
    name_cn = Column(Unicode(20))
    name_en = Column(String(80))

