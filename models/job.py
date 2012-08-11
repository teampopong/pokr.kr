from sqlalchemy import Column, Date, ForeignKey, Integer, Unicode
from models.base import Base

class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, autoincrement=True, primary_key=True)
    person_id = Column(Integer, ForeignKey('people.id'))
    company = Column(Unicode(60))
    position = Column(Unicode(20))
    startdate = Column(Date)
    enddate = Column(Date)

