# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from datetime import datetime
import json
from glob import glob
import re
import sys

from sqlalchemy.sql.expression import and_
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from conf.storage import DIRS, REDIS_SETTINGS, REDIS_KEYS
from database import transaction
from models.bill import assembly_id_by_bill_id, Bill
from models.bill_status import BillStatus
from models.bill_review import BillReview
from models.election import Election
from models.cosponsorship import cosponsorship
from models.candidacy import Candidacy
from models.person import Person
from queue import RedisQueue


__all__ = ['insert_bills', 'update_bills']


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
        self.last_id_in_db = self.last_id = bss[-1].id
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


def insert_bills():
    queue = RedisQueue(REDIS_KEYS['insert_bills_db'], **REDIS_SETTINGS)
    if queue.empty():
        return

    with transaction() as session:
        _update_bills(session, queue)


def update_bills():
    with transaction() as session:
        assembly_id = session.query(Election)\
                             .order_by(Election.age.desc())\
                             .first()
        # FIXME: filter finished bills out
        bill_ids = (record[0] for record in session.query(Bill.id))
        _update_bills(session, bill_ids)


def _update_bills(session, bill_ids):
    bill_statuses.init(session)
    for bill_id in bill_ids:
        filepath = bill_filepath(bill_id)
        with open(filepath, 'r') as f:
            record = json.load(f)
        insert_bill(session, record)
    bill_statuses.insert_all()


def bill_filepath(bill_id):
    assembly_id = assembly_id_by_bill_id(bill_id)
    return '%s/%d/%s.json' % (DIRS['data'], assembly_id, bill_id)


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
        'age': assembly_id,
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


def insert_cosponsorships(session, bill, cosponsors_raw):
    existing_cosponsor_ids = [c.id for c in bill.cosponsors]
    cosponsorships = []
    for proposer in cosponsors_raw:
        key = (proposer, bill.age)
        if key not in person_ids:
            try:
                person = guess_person(session, proposer, bill.age)

            except Exception, e:
                person = None
                print proposer.encode('utf-8'), e

            person_ids[key] = person.id if person else None

        person_id = person_ids[key]

        if person_id and person_id not in existing_cosponsor_ids:
            cosponsorships.append({
                'person_id': person_id,
                'bill_id': bill.id,
            })

    if cosponsorships:
        session.execute(cosponsorship.insert(), cosponsorships)


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


def guess_person(session, name, assembly_id):
    try:
        person = session.query(Person)\
                        .filter_by(name=name)\
                        .join(Person.candidacies)\
                        .filter(and_(Candidacy.age == assembly_id))\
                        .one()

    except MultipleResultsFound, e:
        person = session.query(Person)\
                        .filter_by(name=name)\
                        .join(Person.candidacies)\
                        .filter(and_(Candidacy.age == assembly_id,
                                     Candidacy.is_elected == True))\
                        .one()
    return person


def parse_date(date_):
    try:
        date_ = datetime.strptime(date_, '%Y-%m-%d').date()
    except:
        date_ = None
    return date_
