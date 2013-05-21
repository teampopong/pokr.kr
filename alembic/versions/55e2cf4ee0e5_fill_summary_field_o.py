# -*- coding: utf-8 -*-

"""fill summary field of bill table

Revision ID: 55e2cf4ee0e5
Revises: 1a6ea068e902
Create Date: 2013-05-21 12:32:53.440153

"""

from __future__ import unicode_literals

# revision identifiers, used by Alembic.
revision = '55e2cf4ee0e5'
down_revision = '1a6ea068e902'

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


bill_t = sa.sql.table(
    'bill',
    sa.sql.column('id', sa.String(20)),
    sa.sql.column('summary', sa.Text),
)


def upgrade():
    for line in open('data/na_bills_19.txt', 'r'):
        bill_raw = json.loads(line)
        bill_id = bill_raw['bill_id']
        summary = bill_raw.get('summaries')
        if summary:
            summary = '\n'.join(summary)

        op.execute(bill_t.update()\
                         .where(bill_t.c.id == bill_id)\
                         .values({
                             'summary': summary
                         })
        )


def downgrade():
    op.execute(bill_t.update()\
                     .values({
                         'summary': None,
                     })
    )
