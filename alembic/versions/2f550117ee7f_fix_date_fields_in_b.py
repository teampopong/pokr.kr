# -*- coding: utf-8 -*-

"""Fix date fields in bill_review table

Revision ID: 2f550117ee7f
Revises: 1b2f289ce63b
Create Date: 2013-05-20 13:56:42.807700

"""

from __future__ import unicode_literals

# revision identifiers, used by Alembic.
revision = '2f550117ee7f'
down_revision = u'1b2f289ce63b'

from datetime import datetime
import json
import re
import sys

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import and_
from os.path import abspath, dirname, join

parentdir = dirname(dirname(dirname(abspath(__file__))))
sys.path.insert(0,parentdir)


date_re = re.compile(r'\d{4}-\d{2}-\d{2}')


bill_review_t = sa.sql.table(
    'bill_review',
    sa.sql.column('id', sa.Integer),
    sa.sql.column('bill_id', sa.String(20)),
    sa.sql.column('name', sa.Unicode(150)),
    sa.sql.column('start_date', sa.Date),
    sa.sql.column('end_date', sa.Date),
)


def upgrade():
    for line in open('data/na_bills_19.txt', 'r'):
        bill_raw = json.loads(line)
        bill_id = bill_raw['bill_id']

        for review_name, review_data in bill_raw['status_dict'].items():
            dates = any_value_with_re(review_data, date_re)
            dates = [datetime.strptime(date_, '%Y-%m-%d').date() for date_ in dates]
            start_date = min(dates) if dates else None
            end_date = max(dates) if dates else None
            op.execute(bill_review_t.update()\
                                    .where(and_(
                                        bill_review_t.c.name == review_name,
                                        bill_review_t.c.bill_id == bill_id
                                    ))\
                                    .values({
                                        'start_date': start_date,
                                        'end_date': end_date,
                                    })
            )


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


def downgrade():
    op.execute(bill_review_t.update()\
                            .values({
                                'start_date': None,
                                'end_date': None,
                            })
    )
