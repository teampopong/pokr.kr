from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer
from models.base import Base

class PersonParty(Base):
    __tablename__ = 'people_parties'

    ### join ###
    id = Column(Integer, autoincrement=True, primary_key=True)
    person_id = Column(Integer, ForeignKey('people.id'))
    party_id = Column(Integer, ForeignKey('parties.id'))

    ### additional infos ###
    start_date = Column(Date)
    end_date = Column(Date)
    is_current_member = Column(Boolean, default=True)

