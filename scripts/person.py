# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from database import transaction
from models.person import Person
from utils.command import Command
from utils.csv import read_csv

__all__ = ['update_people']


class PersonCommand(Command):
    __command__ = 'person'


class UpdatePeopleCommand(Command):
    __command__ = 'update'
    __parent__ = PersonCommand

    @classmethod
    def init_parser_options(cls):
        cls.parser.add_argument('filename', nargs=1)

    @classmethod
    def run(cls, filename, **kwargs):
        update_people(filename=filename)


def update_people(filename):
    if not filename:
        return

    with transaction() as session:
        headers, records = read_csv(filename, headers=True)
        for record in records:
            update_person(session, headers, record)


def update_person(session, headers, record):
    person = session.query(Person).filter_by(id=record['person_id']).first()
    person_data = extract_person(headers, record)
    if person:
        for key, val in person_data.items():
            if key != 'id':
                setattr(person, key, val)
    else:
        person = Person(**person_data)
        session.add(person)


def extract_person(headers, record):
    raise NotImplementedError()
