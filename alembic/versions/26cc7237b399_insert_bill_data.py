"""insert bill data

Revision ID: 26cc7237b399
Revises: 42b10177639f
Create Date: 2013-05-03 16:29:34.794322

"""

# revision identifiers, used by Alembic.
revision = '26cc7237b399'
down_revision = '42b10177639f'

from datetime import datetime
import json
from os.path import abspath, dirname, join

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from models.person import Person


proj_dir = dirname(dirname(dirname(abspath(__file__))))
bills_path = join(proj_dir, 'data/na_bills_18.json')
bill_url_format = 'http://data.popong.com/bills/{filename}'


bill_t = sa.sql.table(
    'bill',
    sa.sql.column('id', sa.String(length=20)),
    sa.sql.column('name', sa.Unicode(length=150)),
    sa.sql.column('age', sa.Integer()),
    sa.sql.column('proposed_date', sa.Date()),
    sa.sql.column('decision_date', sa.Date()),
    sa.sql.column('proposers', postgresql.ARRAY(sa.Unicode(length=100))),
    sa.sql.column('proposer_representative', sa.Unicode(length=100)),
    sa.sql.column('committee', sa.Unicode(length=100)),
    sa.sql.column('proposer_type', sa.Integer()),
    sa.sql.column('status', sa.Integer()),
    sa.sql.column('status_detail', sa.Unicode(length=10)),
    sa.sql.column('link_id', sa.String(length=40)),
    sa.sql.column('attachments', postgresql.ARRAY(sa.String(length=1024))),
)


def upgrade():
    with open(bills_path, 'r') as f:
        bills = json.load(f)

    for bill in bills:
        insert_bill(bill)


def downgrade():
    op.execute(bill_t.delete())


def insert_bill(bill):
    preprocess(bill)
    op.execute(bill_t.insert().values(**bill))


def preprocess(bill):
    bill['id'] = bill['bill_id']
    del bill['bill_id']

    if bill['proposer']:
        bill['proposers'] = list(bill['proposer'])
    del bill['proposer']

    if bill['proposed_date']:
        bill['proposed_date'] = parse_time(bill['proposed_date'])

    if bill['decision_date']:
        bill['decision_date'] = parse_time(bill['decision_date'])

    bill['attachments'] = [bill_url_format.format(filename=filename)
                           for filename in bill['attachments']]


def parse_time(date_string):
    return datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
