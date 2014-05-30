# -*- coding: utf-8 -*-

from flask import url_for
from sqlalchemy import Column, ForeignKey, func, Integer, select, Text
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import column_property

from pokr.models import Meeting
from pokr.database import Base


class Statement(Base):
    __tablename__ = 'statement'

    id = Column(Integer, autoincrement=True, primary_key=True)
    meeting_id = Column(ForeignKey('meeting.id'), nullable=False, index=True)
    person_id = Column(ForeignKey('person.id'), index=True)

    sequence = Column(Integer, nullable=False)
    speaker = Column(Text)
    content = Column(Text)

    date = column_property(select([Meeting.date])\
                           .where(Meeting.id==meeting_id), deferred=True)

    @property
    def url(self):
        return url_for('meeting', id=self.meeting_id)

    @hybrid_property
    def anchor(self):
        return '{0}-{1}'.format(person_id, sequence)

    @anchor.expression
    def anchor(self):
        return func.concat(person_id, '-', sequence)

