# -*- coding: utf-8 -*-

"""Insert 17~18th na bills

Revision ID: 45205c4e6bd8
Revises: 55e2cf4ee0e5
Create Date: 2013-05-22 10:27:56.780786

"""

from __future__ import unicode_literals

# revision identifiers, used by Alembic.
revision = '45205c4e6bd8'
down_revision = '17b5e9dda9a0'

from datetime import datetime
import json
import re
import sys

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql.expression import and_
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from os.path import abspath, dirname, join

parentdir = dirname(dirname(dirname(abspath(__file__))))
sys.path.insert(0,parentdir)
from models.bill_status import BillStatus
from models.candidacy import Candidacy
from models.person import Person


ws_re = re.compile(r'\s+')
date_re = re.compile(r'\d{4}-\d{2}-\d{2}')


bill_t = sa.sql.table(
    'bill',
    sa.sql.column('id', sa.String(20)),
    sa.sql.column('name', sa.Unicode(256)),
    sa.sql.column('age', sa.Integer),
    sa.sql.column('proposed_date', sa.Date),
    sa.sql.column('decision_date', sa.Date),
    sa.sql.column('is_processed', sa.Boolean),
    sa.sql.column('link_id', sa.String(40)),
    sa.sql.column('sponsor', sa.Unicode(80)),
    sa.sql.column('summary', sa.Text()),
    sa.sql.column('status_id', sa.Integer),
    sa.sql.column('status_ids', ARRAY(sa.Integer)),
)

cosponsorship_t = sa.sql.table(
    'cosponsorship',
    sa.sql.column('id', sa.Integer),
    sa.sql.column('person_id', sa.Integer),
    sa.sql.column('bill_id', sa.String(20)),
    sa.sql.column('is_sponsor', sa.Boolean),
)

bill_review_t = sa.sql.table(
    'bill_review',
    sa.sql.column('id', sa.Integer),
    sa.sql.column('bill_id', sa.String(20)),
    sa.sql.column('name', sa.Unicode(150)),
    sa.sql.column('start_date', sa.Date),
    sa.sql.column('end_date', sa.Date),
    sa.sql.column('data', sa.Text),
)

bill_status_t = sa.sql.table(
    'bill_status',
    sa.sql.column('id', sa.Integer),
    sa.sql.column('name', sa.Unicode(150)),
)


bill_status_ids = {}
person_ids = {}
last_bill_status_id = 0
orig_last_bill_status_id = 0


def upgrade():
    setup()
    insert_bills(17)
    insert_bills(18)
    insert_bill_statuses()


def insert_bill_statuses():
    bill_statuses = [{
                         'id': id,
                         'name': name
                     } for name, id in bill_status_ids.items()
                       if id > orig_last_bill_status_id]
    if bill_statuses:
        op.bulk_insert(bill_status_t, bill_statuses)


def setup():
    bss = BillStatus.query.order_by(BillStatus.id).all()
    global bill_status_ids
    bill_status_ids = {
        bs.name: bs.id
        for bs in bss
    }
    global last_bill_status_id
    global orig_last_bill_status_id
    orig_last_bill_status_id = last_bill_status_id = bss[-1].id


def insert_bills(assembly_id):
    print 'processing bills of %dth assembly' % assembly_id

    for line in open('data/na_bills_%d.txt' % assembly_id, 'r'):
        bill_raw = json.loads(line)
        validate(bill_raw)

        bill_id = bill_raw['bill_id']
        name = bill_raw['title']
        proposed_date = bill_raw['proposed_date']
        decision_date = bill_raw['decision_date']
        is_processed = bill_raw['status'] == '처리'
        link_id = bill_raw['link_id']
        sponsor = bill_raw['status_dict']['접수']['의안접수정보'][0]['제안자']
        while isinstance(sponsor, list):
            sponsor = sponsor[0]
        summary = bill_raw.get('summaries')
        if summary:
            summary = '\n'.join(summary)
        status_ids = [bill_status_id(status) for status in bill_raw['statuses']]
        status_id = bill_status_id(bill_raw['status_detail'])

        op.execute(bill_t.insert().values({
            'id': bill_id,
            'name': name,
            'age': assembly_id,
            'proposed_date': proposed_date,
            'decision_date': decision_date,
            'is_processed': is_processed,
            'link_id': link_id,
            'sponsor': sponsor,
            'summary': summary,
            'status_ids': status_ids,
            'status_id': status_id,
        }))

        cosponsorships = []
        for proposer in bill_raw['proposers']:
            if proposer not in person_ids:
                try:
                    person = guess_person(proposer, assembly_id)

                except Exception, e:
                    person = None
                    print proposer, e

                person_ids[proposer] = person.id if person else None

            person_id = person_ids[proposer]

            if person_id:
                cosponsorships.append({
                    'person_id': person_id,
                    'bill_id': bill_id,
                })

        if cosponsorships:
            op.bulk_insert(cosponsorship_t, cosponsorships)

        reviews = []
        for review_name, review_data in bill_raw['status_dict'].items():
            dates = any_value_with_re(review_data, date_re)
            dates = [datetime.strptime(date_, '%Y-%m-%d').date() for date_ in dates]
            start_date = min(dates) if dates else None
            end_date = max(dates) if dates else None
            reviews.append({
                'name': review_name,
                'bill_id': bill_id,
                'start_date': start_date,
                'end_date': end_date,
                'data': json.dumps(review_data)
            })

        if reviews:
            op.bulk_insert(bill_review_t, reviews)


def bill_status_id(status):
    status = ws_re.sub('', status)
    if status not in bill_status_ids:
        global last_bill_status_id
        last_bill_status_id += 1
        bill_status_ids[status] = last_bill_status_id
    return bill_status_ids[status]


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


def guess_person(name, assembly_id):
    try:
        person = Person.query\
                        .filter_by(name=name)\
                        .join(Person.candidacies)\
                        .filter(and_(Candidacy.age == assembly_id))\
                        .one()

    except MultipleResultsFound, e:
        person = Person.query\
                        .filter_by(name=name)\
                        .join(Person.candidacies)\
                        .filter(and_(Candidacy.age == assembly_id,
                                     Candidacy.is_elected == True))\
                        .one()
    return person


def validate(bill):
    if bill['status'] not in ['처리', '계류']:
        raise Exception()


def downgrade():
    op.execute(bill_t.delete().where(bill_t.c.age.in_((17, 18))))
