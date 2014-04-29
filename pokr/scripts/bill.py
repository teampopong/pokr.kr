# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import argparse
from datetime import datetime
import json
from glob import glob
import re
import sys

from sqlalchemy.sql.expression import and_

from settings import BILLJSON_DIR, REDIS_SETTINGS, REDIS_KEYS
from pokr.database import transaction
from pokr.models.bill import assembly_id_by_bill_id, Bill
from pokr.models.bill_status import BillStatus
from pokr.models.bill_review import BillReview
from pokr.models.election import Election
from pokr.models.cosponsorship import cosponsorship
from pokr.models.candidacy import Candidacy
from pokr.models.person import guess_person, Person
from pokr.queue import RedisQueue
from utils.command import Command


__all__ = ['update_bills']


class BillCommand(Command):
    __command__ = 'bill'


class UpdateBillsCommand(Command):
    __command__ = 'update'
    __parent__ = BillCommand

    @classmethod
    def init_parser_options(cls):
        cls.parser.add_argument('files', nargs='*')
        cls.parser.add_argument('--source', dest='source', nargs='?',
                default='files',
                help='source of the bill IDs to be updated (redis/db/files)')

    @classmethod
    def run(cls, source, files, **kwargs):
        update_bills(source, files=files)


class BillStatusStore(object):
    dict_ = {}
    last_id = 0
    last_id_in_db = 0

    def __init__(self, session=None):
        if session:
            self.init(session)

    def init(self, session):
        bss = session.query(BillStatus).order_by(BillStatus.id).all()
        self.dict_ = {
            bs.name: bs.id
            for bs in bss
        }
        self.last_id_in_db = self.last_id = bss[-1].id if bss else 0
        self.session = session

    def id(self, name):
        name = no_ws(name)
        if name not in self.dict_:
            self.last_id += 1
            self.dict_[name] = self.last_id
        return self.dict_[name]

    def insert_all(self):
        bill_statuses = [{
                             'id': id,
                             'name': name
                         } for name, id in self.dict_.items()
                           if id > self.last_id_in_db]
        if bill_statuses:
            self.session.execute(BillStatus.__table__.insert(), bill_statuses)


date_re = re.compile(r'\d{4}-\d{2}-\d{2}')
ws_re = re.compile(r'\s+')
person_ids = {}
bill_statuses = BillStatusStore()


def update_bills(source, files=None):
    if source == 'redis':
        queue = RedisQueue(REDIS_KEYS['insert_bills_db'], **REDIS_SETTINGS)
        files = (bill_filepath(bill_id) for bill_id in queue)

    elif source.startswith('db'):
        with transaction() as session:
            assembly_id = session.query(Election)\
                                 .order_by(Election.assembly_id.desc())\
                                 .first().assembly_id

        # FIXME: filter finished bills out
        bill_ids = (record[0] for record
                              in session.query(Bill.id)\
                                        .filter_by(assembly_id=assembly_id))

        # ranged query
        m = re.match(r'db\[(\d*):(\d*)\]', source)
        if m:
            start, end = m.group(1), m.group(2)
            offset = int(start) if start else 0
            limit = int(end) - offset if end else None
            if offset:
                bill_ids = bill_ids.offset(offset)
            if limit:
                bill_ids = bill_ids.limit(limit)

        files = (bill_filepath(bill_id) for bill_id in bill_ids)

    elif files:
        files = [f for path in files for f in glob(path)]

    update_bills_from_files(files)


def update_bills_from_files(files):
    if not files:
        return

    with transaction() as session:
        bill_statuses.init(session)
        for f in files:
            try:
                if not isinstance(f, file):
                    f = open(f, 'r')
                with f:
                    record = json.load(f)
            except e:
                print >> sys.stderr, e
                continue
            insert_bill(session, record)
        bill_statuses.insert_all()


def bill_filepath(bill_id):
    assembly_id = assembly_id_by_bill_id(bill_id)
    return '%s/%d/%s.json' % (BILLJSON_DIR, assembly_id, bill_id)


def insert_bill(session, record):
    bill = session.query(Bill).filter_by(id=record['bill_id']).first()
    bill_data = extract_bill(record)
    if bill:
        for key, val in bill_data.items():
            if key != 'id':
                setattr(bill, key, val)
    else:
        bill = Bill(**bill_data)
        session.add(bill)
    session.flush()
    insert_cosponsorships(session, bill, record['proposers'])
    insert_reviews(session, bill, record['status_dict'])


def extract_bill(record):
    if record['status'] not in ['처리', '계류']:
        raise Exception()

    assembly_id = record['assembly_id']
    bill_id = record['bill_id']
    name = record['title']

    proposed_date = parse_date(record['proposed_date'])
    decision_date = parse_date(record['decision_date'])
    is_processed = record['status'] == '처리'
    link_id = record['link_id']
    sponsor = record['status_dict']['접수']['의안접수정보'][0]['제안자']
    while isinstance(sponsor, list):
        sponsor = sponsor[0]
    try:
        document_url = record['status_dict']['접수']['의안접수정보'][0]['문서'][0][1][1]
    except:
        try:
            document_url = record['status_dict']['접수']['의안접수정보'][0]['의안원문'][0][1][1]
        except:
            document_url = None
    summary = record.get('summaries')
    summary = '\n'.join(summary) if summary else None
    status_ids = [bill_statuses.id(status) for status in record['statuses']]
    status_id = bill_statuses.id(record['status_detail'])

    return {
        'id': bill_id,
        'name': name,
        'assembly_id': assembly_id,
        'proposed_date': proposed_date,
        'decision_date': decision_date,
        'is_processed': is_processed,
        'link_id': link_id,
        'document_url': document_url,
        'sponsor': sponsor,
        'summary': summary,
        'status_ids': status_ids,
        'status_id': status_id,
    }


def insert_cosponsorships(session, bill, cosponsors):
    try:
        if isinstance(cosponsors[0], dict):
            cosponsors = [c['name_kr'] for c in cosponsors]
    except IndexError:
        pass

    existing_cosponsor_ids = [c.id for c in bill.cosponsors]
    cosponsor_ids = []
    for proposer in cosponsors:
        key = (proposer, bill.assembly_id)
        if key not in person_ids:
            try:
                person = guess_person(session, proposer, bill.assembly_id)

            except Exception, e:
                person = None
                print proposer.encode('utf-8'), e

            person_ids[key] = person.id if person else None

        person_id = person_ids[key]
        if person_id:
            cosponsor_ids.append(person_id)

    set_original, set_current = set(existing_cosponsor_ids), set(cosponsor_ids)
    ids_to_insert = list(set_current - set_original)
    ids_to_delete = list(set_original - set_current)

    if ids_to_insert:
        session.execute(cosponsorship.insert(), [
            {
                'person_id': person_id,
                'bill_id': bill.id,
            } for person_id in ids_to_insert
        ])

    if ids_to_delete:
        session.execute(
            cosponsorship.delete().where(
                and_(cosponsorship.c.person_id.in_(ids_to_delete),
                     cosponsorship.c.bill_id == bill.id)
            )
        )


def insert_reviews(session, bill, reviews_raw):
    reviews = []
    existing_review_names = [r.name for r in bill.reviews]
    for review_name, review_data in reviews_raw.items():
        if review_name in existing_review_names:
            continue

        dates = any_value_with_re(review_data, date_re)
        dates = [datetime.strptime(date_, '%Y-%m-%d').date() for date_ in dates]
        start_date = min(dates) if dates else None
        end_date = max(dates) if dates else None
        reviews.append({
            'name': review_name,
            'bill_id': bill.id,
            'start_date': start_date,
            'end_date': end_date,
            'data': json.dumps(review_data)
        })

    if reviews:
        session.execute(BillReview.__table__.insert(), reviews)


def no_ws(string):
    return ws_re.sub('', string)


def any_value_with_re(obj, regex):

    if isinstance(obj, list):
        items = obj
    elif isinstance(obj, dict):
        items = obj.values()
    else:
        items = []

    res = []
    for val in items:
        if hasattr(val, 'capitalize') and regex.match(val):
            res.append(val)
        else:
            res.extend(any_value_with_re(val, regex))

    return res


def parse_date(date_):
    try:
        date_ = datetime.strptime(date_, '%Y-%m-%d').date()
    except:
        date_ = None
    return date_
