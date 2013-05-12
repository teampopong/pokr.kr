"""Insert address data into person table

Revision ID: 4b053946ef00
Revises: 534f7c1fb55f
Create Date: 2013-05-12 14:38:08.629094

"""

# revision identifiers, used by Alembic.
revision = '4b053946ef00'
down_revision = '534f7c1fb55f'

import json
import sys
from os.path import abspath, dirname, join

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

parentdir = dirname(dirname(dirname(abspath(__file__))))
sys.path.insert(0,parentdir)
from models.person import Person
from utils.nlp.structurizer import markup


person_t = sa.sql.table(
    'person',
    sa.sql.column('id', sa.Integer),
    sa.sql.column('address', postgresql.ARRAY(sa.Unicode(20))),
    sa.sql.column('address_id', postgresql.ARRAY(sa.String(16)))
)


def upgrade():
    people = Person.query
    for person in people:
        try:
            extra_vars = json.loads(person.extra_vars)
        except ValueError, e:
            continue

        if not extra_vars.get('address'):
            continue

        structurized = markup(extra_vars['address'], 'district')

        op.execute(person_t.update().\
                where(person_t.c.id == person.id).\
                values({
                    person_t.c.address: [term[0] for term in structurized],
                    person_t.c.address_id: [term[1] for term in structurized],
                })
        )


def downgrade():
    op.execute(person_t.update()\
            .values({
                person_t.c.address: [],
                person_t.c.address_id: [],
            })
    )

