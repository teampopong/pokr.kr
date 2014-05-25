# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import argparse
from datetime import datetime
import json
import logging
import hashlib

from popong_models import Base
from popong_data_utils import guess_person
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from pokr.database import db_session, transaction
from pokr.models import Meeting, Person, Statement
from utils.command import Command


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


def insert_meetings(region_id, obj):
    if isinstance(obj, dict):
        insert_meeting(obj)

    elif isinstance(obj, list):
        for o in obj:
            insert_meeting(region_id, o)

    else:
        raise Exception()


def insert_meeting(region_id, obj):
    date = datetime.strptime(obj['date'], '%Y-%m-%d').date()
    dialogue = obj['dialogue']
    attendee_names = obj['attendance']['출석 의원']['names']
    id = int('{region_id}{assembly_id}{session_id}{meeting_id}{md5}'.format(
             region_id=region_id,
             md5=int(hashlib.md5(obj['committee'].encode('utf-8')).hexdigest()[:4], 16),
             **obj))

    meeting = Meeting(
        id=id,
        region_id=region_id,
        committee=obj['committee'],
        parliament_id=obj['assembly_id'],
        session_id=obj['session_id'],
        sitting_id=obj['meeting_id'],
        date=date,
        issues=obj['issues'],
        url=obj['issues_url'],
        pdf_url=obj['pdf'],
    )
    with transaction() as session:
        session.add(meeting)

        # 'meeting_attendee' table
        attendees = list(get_attendees(meeting, attendee_names, session))
        meeting.attendees = attendees

        # 'statement' table
        statements = (stmt for stmt in dialogue
                           if stmt['type'] == 'statement')
        for seq, statement in enumerate(statements):
            item = create_statement(meeting, seq, statement, attendees)
            statement['person_id'] = item.person_id
            meeting.statements.append(item)

        # Updated dialog field of meeting table
        meeting.dialogue = dialogue

        # TODO: votes = obj['votes']


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


def guess_attendee(attendees, name):
    for attendee in attendees:
        if attendee.name in name:
            return attendee
    return None

