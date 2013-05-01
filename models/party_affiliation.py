from sqlalchemy import CHAR, Boolean, Column, ForeignKey, Integer, Table
from database import Base

party_affiliation = Table('party_affiliation', Base.metadata,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('person_id', Integer, ForeignKey('person.id'), nullable=False),
    Column('party_id', Integer, ForeignKey('party.id'), nullable=False),
    Column('start_date', CHAR(8)),
    Column('end_date', CHAR(8)),
    Column('is_current_member', Boolean, default=True, index=True),
)
