# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, Integer, Enum

from pokr.database import Base


class MeetingStatementVote(Base):
    __tablename__ = 'meeting_statement_vote'

    id = Column(Integer, autoincrement=True, primary_key=True)
    meeting_id = Column(ForeignKey('meeting.id'), nullable=False, index=True)
    statement_id = Column(ForeignKey('statement.id'), nullable=False, index=True)
    person_id = Column(ForeignKey('person.id'), nullable=False, index=True)
    vote = Column(Enum('yea', 'nay', 'forfeit', name='enum_meeting_statement_vote_type'), nullable=False, index=True)
