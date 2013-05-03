"""empty message

Revision ID: 2507366cb6f2
Revises: 2a31d97fa618
Create Date: 2013-04-30 00:11:14.194453

"""

# revision identifiers, used by Alembic.
revision = '2507366cb6f2'
down_revision = '2a31d97fa618'

from os.path import abspath, dirname, join
import sys

from alembic import op
import sqlalchemy as sa

parentdir = dirname(dirname(dirname(abspath(__file__))))
sys.path.insert(0,parentdir)
from models.person import Person
from utils.nlp.utils.translit import translit


person_t = sa.sql.table(
    'person',
    sa.sql.column('id', sa.Integer),
    sa.sql.column('name', sa.Unicode(20)),
    sa.sql.column('name_en', sa.String(80))
)


def upgrade():
    people = Person.query.all()
    for person in people:
        name_en = translit(person.name, 'ko', 'en', 'name')
        op.execute(person_t.update().\
                where(person_t.c.id == person.id).\
                values({'name_en': op.inline_literal(name_en)})
        )


def downgrade():
    op.execute(person_t.update().\
            values({'name_en': op.inline_literal('')})
    )
