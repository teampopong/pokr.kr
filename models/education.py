# -*- coding: utf-8 -*-

from sqlalchemy import Table, Column, Enum, ForeignKey, Integer, Unicode
from database import Base

courses = ['elementary', 'middle', 'high', 'undergrad', 'grad']
statuses = ['in', 'dropped', 'graduated', 'completed']

education = Table('education', Base.metadata,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('person_id', Integer, ForeignKey('person.id'), nullable=False),
    Column('school_id', Integer, ForeignKey('school.id'), nullable=False),

    # additional infos
    Column('course', Enum(*courses, name='enum_education_course'), index=True),
    Column('mayor', Unicode(20)),
    Column('start_year', Integer, index=True),
    Column('end_year', Integer),
    Column('status', Enum(*statuses, name='enum_education_status')),
)
