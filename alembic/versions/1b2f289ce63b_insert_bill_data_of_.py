# -*- coding: utf-8 -*-

"""Insert bill data of 19th assembly

Revision ID: 1b2f289ce63b
Revises: 80674dad104
Create Date: 2013-05-19 22:08:48.699372

"""

from __future__ import unicode_literals

# revision identifiers, used by Alembic.
revision = '1b2f289ce63b'
down_revision = '80674dad104'

from datetime import date
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
from models.candidacy import Candidacy
from models.person import Person


ws_re = re.compile(r'\s+')
date_re = re.compile(r'\d{4}-\d{2}-\d{2}')


bill_t = sa.sql.table(
    'bill',
    sa.sql.column('id', sa.String(20)),
    sa.sql.column('name', sa.Unicode(150)),
    sa.sql.column('age', sa.Integer),
    sa.sql.column('proposed_date', sa.Date),
    sa.sql.column('decision_date', sa.Date),
    sa.sql.column('is_processed', sa.Boolean),
    sa.sql.column('link_id', sa.String(40)),
    sa.sql.column('sponsor', sa.Unicode(20)),
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


def upgrade():
    for line in open('data/na_bills_19.txt', 'r'):
        bill_raw = json.loads(line)
        validate(bill_raw)

        bill_id = bill_raw['bill_id']
        name = bill_raw['title']
        age = 19
        proposed_date = bill_raw['proposed_date']
        decision_date = bill_raw['decision_date']
        is_processed = bill_raw['status'] == '처리'
        link_id = bill_raw['link_id']
        sponsor = bill_raw['status_dict']['접수']['의안접수정보'][0]['제안자']
        while isinstance(sponsor, list):
            sponsor = sponsor[0]
        status_ids = [bill_status_id(status) for status in bill_raw['statuses']]
        status_id = bill_status_id(bill_raw['status'])

        op.execute(bill_t.insert().values({
            'id': bill_id,
            'name': name,
            'age': age,
            'proposed_date': proposed_date,
            'decision_date': decision_date,
            'is_processed': is_processed,
            'link_id': link_id,
            'sponsor': sponsor,
            'status_ids': status_ids,
            'status_id': status_id,
        }))

        for proposer in bill_raw['proposers']:
            if proposer not in person_ids:
                try:
                    person = guess_person(proposer)

                except Exception, e:
                    person = None
                    print proposer, e

                person_ids[proposer] = person.id if person else None

            person_id = person_ids[proposer]

            if person_id:
                op.execute(cosponsorship_t.insert().values({
                    'person_id': person_id,
                    'bill_id': bill_id,
                }))

        for review_name, review_data in bill_raw['status_dict'].items():
            dates = any_value_with_re(review_data, date_re)
            dates = [date.strptime(date_, '%Y-%m-%d') for date in dates]
            start_date = min(dates) if dates else None
            end_date = max(dates) if dates else None
            op.execute(bill_review_t.insert().values({
                'name': review_name,
                'bill_id': bill_id,
                'start_date': start_date,
                'end_date': end_date,
                'data': json.dumps(review_data)
            }))

    for bill_status, id in bill_status_ids.items():
        op.execute(bill_status_t.insert().values({
            'id': id,
            'name': bill_status,
        }))


def bill_status_id(status):
    status = ws_re.sub('', status)
    if status not in bill_status_ids:
        global last_bill_status_id
        last_bill_status_id += 1
        bill_status_ids[status] = last_bill_status_id
    return bill_status_ids[status]


def any_value_with_re(obj, regex):
    res = []
    for key, val in obj.items():
        if isinstance(val, str) and regex.match(val):
            res.append(val)
        elif isinstance(val, dict):
            res.extend(any_value_with_re(val, regex))
    return res


def guess_person(name):
    try:
        person = Person.query\
                        .filter_by(name=name)\
                        .join(Person.candidacies)\
                        .filter(and_(Candidacy.age == 19))\
                        .one()

    except MultipleResultsFound, e:
        person = Person.query\
                        .filter_by(name=name)\
                        .join(Person.candidacies)\
                        .filter(and_(Candidacy.age == 19,
                                     Candidacy.is_elected == True))\
                        .one()
    return person


def validate(bill):
    if bill['status'] not in ['처리', '계류']:
        raise Exception()


def downgrade():
    op.execute(cosponsorship_t.delete())
    op.execute(bill_review_t.delete())
    op.execute(bill_status_t.delete())
    op.execute(bill_t.delete())
