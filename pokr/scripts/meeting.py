# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import argparse
from datetime import datetime
import hashlib
import json
import logging
import re

from popong_models import Base
from popong_data_utils import guess_person
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from pokr.database import db_session, transaction
from pokr.models import Meeting, Person, Statement
from utils.command import Command


attendance_re = re.compile(r'(출|참)석\s*(감사위|의|위)원')


class MeetingCommand(Command):
    __command__ = 'meeting'


class InsertMeetingCommand(Command):
    __command__ = 'insert'
    __parent__ = MeetingCommand

    @classmethod
    def init_parser_options(cls):
        cls.parser.add_argument('files', type=argparse.FileType('r'), nargs='+')
        cls.parser.add_argument('-r', dest='region_id', required=True)

    @classmethod
    def run(cls, files, region_id, **kwargs):
        Base.query = db_session.query_property()
        for file_ in files:
            obj = json.load(file_)
            insert_meetings(region_id, obj)


class UpdateMeetingCommand(Command):
    __command__ = 'update'
    __parent__ = MeetingCommand

    @classmethod
    def init_parser_options(cls):
        cls.parser.add_argument('files', type=argparse.FileType('r'), nargs='+')
        cls.parser.add_argument('-r', dest='region_id', required=True)

    @classmethod
    def run(cls, files, region_id, **kwargs):
        Base.query = db_session.query_property()
        for file_ in files:
            obj = json.load(file_)
            insert_meetings(region_id, obj, update=True)


def insert_meetings(region_id, obj, update=False):
    try:
        if isinstance(obj, dict):
            insert_meeting(region_id, obj, update)

        elif isinstance(obj, list):
            for o in obj:
                insert_meeting(region_id, o, update)
        else:
            raise Exception()
    except KeyError, e:
        logging.warn('KeyError: %s' % e)


def strhash(s, len=4):
    if isinstance(s, unicode):
        s = s.encode('utf-8')
    return int(hashlib.md5(s).hexdigest()[:len], 16)


def create_or_get_meeting(session, region_id, obj, update=False):
    date = datetime.strptime(obj['date'], '%Y-%m-%d').date()
    session_id = obj['session_id'] or ''
    meeting_id = obj['meeting_id'] or ''
    id = int('{region_id}{assembly_id}{session_id}{meeting_id}{md5}'.format(
             region_id=region_id,
             assembly_id=obj['assembly_id'],
             session_id=int(session_id) if session_id.isdigit() else strhash(session_id),
             meeting_id=int(meeting_id) if meeting_id.isdigit() else strhash(meeting_id),
             md5=strhash(obj['committee'])))

    meeting = session.query(Meeting).filter_by(id=id).first()
    if not update and meeting:
        logging.info('Skip {id}'.format(id=id))
        return
    if not meeting:
        meeting = Meeting(
            id=id,
            region_id=region_id,
            committee=obj['committee'],
            parliament_id=obj['assembly_id'],
            session_id=session_id,
            sitting_id=meeting_id,
            date=date,
            issues=obj['issues'],
            url='',
            pdf_url=obj['pdf'],
        )
    return meeting


def insert_meeting(region_id, obj, update=False):

    with transaction() as session:
        meeting = create_or_get_meeting(session, region_id, obj, update)
        if not meeting:
            return
        session.add(meeting)

        # 'meeting_attendee' table
        attendee_names = get_attendee_names(obj)
        attendees = list(get_attendees(meeting, attendee_names, session))
        meeting.attendees = attendees

        # clear the meeting's statements
        for statement in meeting.statements:
            session.delete(statement)
        session.flush()
        meeting.statements = []

        # 'statement' table
        statements = (stmt for stmt in obj['dialogue']
                           if stmt['type'] == 'statement')
        for seq, statement in enumerate(statements):
            item = create_statement(meeting, seq, statement, attendees)
            session.add(item)
            session.flush()
            statement['person_id'] = item.person_id
            statement['id'] = item.id
            meeting.statements.append(item)

        # Updated dialog field of meeting table
        meeting.dialogue = obj['dialogue']

        # TODO: votes = obj['votes']
        # The following code should be reviewed
        meeting.votes = []
        options = ['yea', 'nay', 'forfeit']
        for option in options:
            if option in stmt['votes']:
                for person_name in stmt['votes'][option]:
                    person = guess_attendee(attendees, person_name)
                    statement = guess_statement(statements, stmt['name'])
                    if person and statement:
                        item = create_vote(meeting, statement, person, option)
                        session.add(item)
                        meeting.votes.append(item)


def get_attendee_names(obj):
    for key, val in obj.get('attendance', {}).iteritems():
        if attendance_re.match(key):
            return val['names']
    logging.warning('Attendance not found {date}-{committee}'.format(**obj))
    return []


def get_attendees(meeting, names, session=None):
    for name in names:
        try:
            person = guess_person(name=name, assembly_id=meeting.parliament_id,
                                  is_elected=True)
            # FIXME: workaround different session binding problem
            yield session.query(Person).filter_by(id=person.id).one()
        except MultipleResultsFound as e:
            logging.warning('Multiple result found for: %s' % name)
        except NoResultFound as e:
            logging.warning('No result found for: %s' % name)


def create_statement(meeting, seq, statement, attendees):
    person = guess_attendee(attendees, statement['person'])
    item = Statement(
        meeting_id=meeting.id,
        person_id=person.id if person else None,
        sequence=seq,
        speaker=statement['person'],
        content=statement['content'],
    )
    return item


def create_vote(meeting, statement, person, option):
    item = MeetingStatementVote(
        meeting_id=meeting.id,
        statement_id=statement['id']
        person_id=person.id,
        vote=option,
    )
    return item


def guess_attendee(attendees, name):
    for attendee in attendees:
        if attendee.name in name:
            return attendee
    return None


def guess_statement(statements, name):
    # Not sure whether it works properly
    for statement in statements:
        if statement.name in name:
            return statement
    return None

