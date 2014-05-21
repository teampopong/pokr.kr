# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, Integer, Text

from pokr.database import Base


class MeetingAttendee(Base):
    __tablename__ = 'meeting_attendee'

    id = Column(Integer, autoincrement=True, primary_key=True)
    meeting_id = Column(ForeignKey('meeting.id'), nullable=False, index=True)
    person_id = Column(ForeignKey('person.id'), nullable=False, index=True)

