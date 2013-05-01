"""Insert education data into person table

Revision ID: 2c793359a1c0
Revises: 2f5c5a76269e
Create Date: 2013-05-02 01:55:04.043930

"""

# revision identifiers, used by Alembic.
revision = '2c793359a1c0'
down_revision = '2f5c5a76269e'

import json

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from models.person import Person
from utils.nlp.structurizer import markup


person_t = sa.sql.table(
    'person',
    sa.sql.column('id', sa.Integer),
    sa.sql.column('education', postgresql.ARRAY(sa.Unicode(60))),
    sa.sql.column('education_id', postgresql.ARRAY(sa.String(20)))
)


def upgrade():
    people = Person.query.all()
    for person in people:
        try:
            extra_vars = json.loads(person.extra_vars)
        except ValueError, e:
            continue

        if not extra_vars.get('education'):
            continue

        structurized = markup(extra_vars['education'], 'education')

        op.execute(person_t.update().\
                where(person_t.c.id == person.id).\
                values({
                    person_t.c.education: [term[0] for term in structurized],
                    person_t.c.education_id: [term[1] for term in structurized],
                })
        )


def downgrade():
    pass
