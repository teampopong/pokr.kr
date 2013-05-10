"""Insert distrct data into candidacy table

Revision ID: 19b8212b017e
Revises: 453b49f6b2b8
Create Date: 2013-05-10 17:39:50.977951

"""

# revision identifiers, used by Alembic.
revision = '19b8212b017e'
down_revision = '453b49f6b2b8'

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


candidacy_t = sa.sql.table(
    'candidacy',
    sa.sql.column('person_id', sa.Integer),
    sa.sql.column('election_id', sa.Integer),
    sa.sql.column('district', postgresql.ARRAY(sa.Unicode(20))),
    sa.sql.column('district_id', postgresql.ARRAY(sa.String(16)))
)


def upgrade():
    for line in open('data/people.json', 'r'):
        person_r = json.loads(line)
        candidacies_r = person_r['assembly']

        person = find_person(person_r)

        for candidacy in person.candidacies:
            election = candidacy.election
            try:
                candidacy_r = candidacies_r[unicode(election.age)]
            except KeyError, e:
                continue

            try:
                structurized = markup(candidacy_r['district'], 'district')
            except Exception, e:
                print candidacy_r['district']
                import sys; sys.exit(1)

            op.execute(candidacy_t.update().\
                    where(candidacy_t.c.person_id == person.id
                          and candidacy_t.c.election_id == election.id).\
                    values({
                        candidacy_t.c.district: [term[0] for term in structurized],
                        candidacy_t.c.district_id: [term[1] for term in structurized],
                    })
            )


def downgrade():
    op.execute(candidacy_t.update().values({
        candidacy_t.c.district: [],
        candidacy_t.c.district_id: []
    }))


def find_person(r):
    r['name_kr'] = r['name_kr'].replace(' ', '')
    person = Person.query.filter_by(name=r['name_kr'], birthday_year=r['birthyear']).one()
    return person
