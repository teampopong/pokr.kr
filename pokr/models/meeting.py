# -*- coding: utf-8 -*-

from datetime import date

from flask.ext.babel import gettext
from sqlalchemy import BigInteger, Column, Date, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSON
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import deferred, relationship
from sqlalchemy.sql.expression import extract

from pokr.database import Base
from pokr.models.meeting_attendee import MeetingAttendee


class Meeting(Base):
    __tablename__ = 'meeting'

    # Identifiers
    id = Column(BigInteger, primary_key=True)
    committee = Column(Text, index=True)
    region_id = Column(ForeignKey('region.id'), index=True)
    parliament_id = Column(Integer, nullable=False, index=True)
    session_id = Column(Integer, index=True)
    sitting_id = Column(Integer, index=True)

    # Meta & contents
    date = Column(Date, nullable=False, index=True)
    issues = deferred(Column(ARRAY(Text)), group='extra')
    dialogue = deferred(Column(JSON), group='extra')
    url = deferred(Column(Text), group='extra')
    pdf_url = deferred(Column(Text), group='extra')

    attendees = relationship('Person',
            secondary=MeetingAttendee.__table__,
            backref='meeting')

    statements = relationship('Statement',
            order_by='Statement.sequence',
            backref='meeting')

    @property
    def title(self):
        r = []
        r.append(gettext('%(parliament_id)dth parliament',
                         parliament_id=self.parliament_id))
        if self.session_id:
            r.append(gettext('%(session_id)dth session',
                             session_id=self.session_id))
        if self.sitting_id:
            r.append(gettext('%(sitting_id)dth sitting',
                             sitting_id=self.sitting_id))
        r.append(self.committee)
        return ' '.join(r)

    @hybrid_property
    def year(self):
        return self.date.year

    @year.expression
    def year(cls):
        return extract('year', cls.date)

