# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import argparse
from datetime import datetime
import json
import logging

from popong_models import Base
from popong_data_utils import guess_person
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from pokr.database import db_session, transaction
from pokr.models.person import Person
from pokr.models.meeting import Meeting
from utils.command import Command


class MeetingCommand(Command):
    __command__ = 'meeting'


class InsertMeetingCommand(Command):
    __command__ = 'insert'
    __parent__ = MeetingCommand

    @classmethod
    def init_parser_options(cls):
        cls.parser.add_argument('files', type=argparse.FileType('r'), nargs='+')

    @classmethod
    def run(cls, files, **kwargs):
        Base.query = db_session.query_property()
        for file_ in files:
            obj = json.load(file_)
            insert_meetings(obj)


def insert_meetings(obj):
    if isinstance(obj, dict):
        insert_meeting(obj)

    elif isinstance(obj, list):
        for o in obj:
            insert_meeting(o)

    else:
        raise Exception()


def insert_meeting(obj):
    date = datetime.strptime(obj['date'], '%Y-%m-%d').date()
    dialogue = obj['dialogue']
    attendee_names = obj['attendance']['출석 의원']['names']

    meeting = Meeting(
        committee=obj['committee'],
        parliament=obj['assembly_id'],
        session=obj['session_id'],
        sitting=obj['meeting_id'],
        date=date,
        issues=obj['issues'],
        dialogue=dialogue,
        url=obj['issues_url'],
        pdf_url=obj['pdf'],
    )
    with transaction() as session:
        session.add(meeting)
        attendees = get_attendees(meeting, attendee_names, session)
        meeting.attendees = list(attendees)
        # TODO: votes = obj['votes']

def get_attendees(meeting, names, session=None):
    for name in names:
        try:
            person = guess_person(name=name, assembly_id=meeting.parliament)
            yield session.query(Person).filter_by(id=person.id).one()
        except MultipleResultsFound as e:
            logging.warning('Multiple result found for: %s' % name)
        except NoResultFound as e:
            logging.warning('No result found for: %s' % name)

