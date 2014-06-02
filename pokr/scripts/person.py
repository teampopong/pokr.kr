# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import argparse
from datetime import date
import json
import logging

from popong_data_utils import connect_db, guess_person
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from pokr.database import db_session, transaction
from pokr.models import Party, PartyAffiliation, Person, Snapshot
from utils.command import Command


class PersonCommand(Command):
    __command__ = 'person'


class UpdatePeopleCommand(Command):
    __command__ = 'update'
    __parent__ = PersonCommand

    @classmethod
    def init_parser_options(cls):
        cls.parser.add_argument('file', type=argparse.FileType('r'))
        cls.parser.add_argument('-d', dest='date', default=date.today())

    @classmethod
    def run(cls, file, date, **kwargs):
        update_people(file, date)


def update_people(fd, date):
    if not fd:
        return

    connect_db(db_session)
    with transaction() as session:
        records = json.load(fd)
        for record in records:
            preprocess_record(record)
            person_id = update_person(session, record)
            if not person_id:
                continue
            party_id = insert_party(session, record['party'])
            insert_party_affiliation(session, person_id, party_id, date)
            # XXX: temporarily disabled
            # TODO: check whether the data changed
            # backup_person(session, record, person_id, date)


def preprocess_record(record):
    record['birthday'] = record.pop('birth').replace('-', '')
    record['image'] = record.pop('photo')


def update_person(session, record):
    name = record['name_kr']
    person = None
    try:
        person = guess_person(name=name,
                              birthday=record['birthday'],
                              is_elected=True)
    except MultipleResultsFound as e:
        logging.warning('Multiple result found for: %s' % name)
    except NoResultFound as e:
        logging.warning('No result found for: %s' % name)

    if not person:
        return

    person = session.query(Person).filter_by(id=person.id).first()
    for key, val in record.items():
        if key != 'id' and hasattr(person, key):
            setattr(person, key, val)

    return person.id


def insert_party(session, name):
    party = session.query(Party).filter_by(name=name).first()
    if not party:
        party = Party(name=name)
        session.add(party)
        session.flush()
    return party.id


def insert_party_affiliation(session, person_id, party_id, date):
    party_affiliation = PartyAffiliation(person_id=person_id, party_id=party_id, date=date)
    session.add(party_affiliation)


def backup_person(session, record, person_id, date):
    data = json.dumps(record)
    snapshot = Snapshot(tablename='person',
                        record_id=str(person_id),
                        date=date.strftime('%y%m%d'),
                        data=data)
    session.add(snapshot)

