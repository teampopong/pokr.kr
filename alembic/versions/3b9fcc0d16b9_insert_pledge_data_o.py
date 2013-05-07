"""Insert pledge data of 19th NA

Revision ID: 3b9fcc0d16b9
Revises: 36c44957687f
Create Date: 2013-05-07 17:26:26.391858

"""

# revision identifiers, used by Alembic.
revision = '3b9fcc0d16b9'
down_revision = '36c44957687f'


import csv
from os.path import dirname, abspath
import sys

from alembic import op
import sqlalchemy as sa

parentdir = dirname(dirname(dirname(abspath(__file__))))
sys.path.insert(0,parentdir)
from models.candidacy import Candidacy
from models.election import Election
from models.person import Person


NA_AGE = 19


pledge_t = sa.sql.table(
    'pledge',
    sa.sql.column('candidacy_id', sa.Integer),
    sa.sql.column('pledge', sa.Unicode(length=128)),
    sa.sql.column('description', sa.UnicodeText),
)


def upgrade():
    with open('data/pledges_19.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            name, party, birthday, pledge, desc = row
            candidacy = find_candidacy(name, birthday, NA_AGE)
            op.execute(pledge_t.insert()\
                               .values({
                                    'candidacy_id': candidacy.id,
                                    'pledge': pledge,
                                    'description': desc
                                })
            )


def find_candidacy(name, birthday, na_age):
    # Compare only birth year because some people have wrong birthday in the DB
    return Candidacy.query\
                    .join(Person,
                          Person.id == Candidacy.person_id)\
                    .filter(Person.name == name,
                            Person.birthday_year == birthday[:4])\
                    .join(Election,
                          Election.id == Candidacy.election_id)\
                    .filter(Election.age == na_age).one()

def downgrade():
    op.execute(pledge_t.delete())
