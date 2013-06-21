"""Insert bill status descriptions

Revision ID: 4a7c4089fc4e
Revises: 3c26b6473d2a
Create Date: 2013-06-21 16:47:59.927372

"""

# revision identifiers, used by Alembic.
revision = '4a7c4089fc4e'
down_revision = '3c26b6473d2a'

import json
from os.path import abspath, dirname, join
import sys

from alembic import op
import sqlalchemy as sa

parentdir = dirname(dirname(dirname(abspath(__file__))))
sys.path.insert(0,parentdir)
from models.bill_status import BillStatus


table = BillStatus.__table__


def upgrade():
    with open('data/statuses.json', 'r') as f:
        statuses = json.load(f)

    for name, desc in statuses.iteritems():
        op.execute(table.update()\
                        .where(table.c.name == name)\
                        .values({
                            table.c.description: desc
                        })
        )


def downgrade():
    op.execute(table.update()\
                    .values({
                        table.c.description: None
                    })
    )
