from sqlalchemy import CHAR, Boolean, Column, ForeignKey, Integer
from database import Base

class PartyAffiliation(Base):
    __tablename__ = 'party_affiliation'

    ### join ###
    id = Column(Integer, autoincrement=True, primary_key=True)
    person_id = Column(Integer, ForeignKey('person.id'), nullable=False)
    party_id = Column(Integer, ForeignKey('party.id'), nullable=False)

    ### additional infos ###
    start_date = Column(CHAR(8))
    end_date = Column(CHAR(8))
    is_current_member = Column(Boolean, default=True, index=True)

    def __init__(self, person_id, party_id, **kwargs):
        self.person_id = person_id
        self.party_id = party_id

        for key, val in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

