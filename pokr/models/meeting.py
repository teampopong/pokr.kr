# -*- coding: utf-8 -*-

from datetime import datetime
import os
import re

from flask.ext.babel import gettext
from sqlalchemy import BigInteger, Column, Date, ForeignKey, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSON
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import deferred, relationship
from sqlalchemy.sql.expression import extract

from pokr.database import Base
from pokr.models.meeting_attendee import MeetingAttendee

from settings import MEETINGPDF_DIR


class Meeting(Base):
    __tablename__ = 'meeting'

    # Identifiers
    id = Column(BigInteger, primary_key=True)
    committee = Column(Text, index=True)
    region_id = Column(ForeignKey('region.id'), index=True)
    parliament_id = Column(Text, nullable=False, index=True)
    session_id = Column(Text, index=True)
    sitting_id = Column(Text, index=True)

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
        r.append(gettext('%(parliament_id)sth parliament',
                         parliament_id=self.parliament_id))

        if self.session_id:
            if self.session_id.isdigit():
                r.append(gettext('%(session_id)sth session',
                                 session_id=self.session_id))
            else:
                r.append(self.session_id)

        if self.sitting_id:
            if self.sitting_id.isdigit():
                r.append(gettext('%(sitting_id)sth sitting',
                                 sitting_id=self.sitting_id))
            else:
                r.append(self.sitting_id)

        r.append(self.committee)
        return ' '.join(r)

    @hybrid_property
    def year(self):
        return self.date.year

    @year.expression
    def year(cls):
        return extract('year', cls.date)

    @property
    def start(self):
        s = self.dialogue[0]
        if s['type']=='time':
            return ':'.join(\
                re.search(ur'([0-9]+)시.*?([0-9]+)분', s['content']).groups())
        return 'Unknown'

    @property
    def end(self):
        e = self.dialogue[-1]
        if e['type']=='time':
            return ':'.join(\
                re.search(ur'([0-9]+)시.*?([0-9]+)분', e['content']).groups())
        return 'Unknown'

    @property
    def duration(self):
        try:
            s = datetime.strptime(self.start, '%H:%M')
            e = datetime.strptime(self.end, '%H:%M')
            return str(e-s)[:-3]
        except ValueError:
            return 'Unknown'

    @property
    def document_pdf_path(self):
        level = 'national'
        filename = '%s-%s-%s-%s.pdf' % (self.parliament_id,
                                        self.session_id,
                                        self.sitting_id,
                                        self.committee)
        filepath = os.path.join(MEETINGPDF_DIR, level,\
                str(self.parliament_id), str(self.date), filename)
        if os.path.exists(filepath):
            return filepath
        else:
            return None
