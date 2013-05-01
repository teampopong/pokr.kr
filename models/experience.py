from sqlalchemy import CHAR, Column, ForeignKey, Integer, Unicode
from database import Base

class Experience(Base):
    __tablename__ = 'experience'

    id = Column(Integer, autoincrement=True, primary_key=True)
    person_id = Column(Integer, ForeignKey('person.id'), nullable=False)
    institution = Column(Unicode(60))
    position = Column(Unicode(20))
    start_date = Column(CHAR(8))
    end_date = Column(CHAR(8))

