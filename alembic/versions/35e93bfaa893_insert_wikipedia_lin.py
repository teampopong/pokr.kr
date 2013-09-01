"""Insert wikipedia links

Revision ID: 35e93bfaa893
Revises: 3aecd12384ee
Create Date: 2013-08-19 16:35:52.127400

"""

# revision identifiers, used by Alembic.
revision = '35e93bfaa893'
down_revision = '3aecd12384ee'

from os.path import abspath, dirname, join

from alembic import op
from models.person import Person
from models.candidacy import Candidacy
from models.election import Election
import sqlalchemy as sa


proj_dir = dirname(dirname(dirname(abspath(__file__))))
wiki_links_path = join(proj_dir, 'data/people-wikipedia-links.csv')


person_t = Person.__table__


def upgrade():
    for line in list(open(wiki_links_path, 'r'))[1:]:
        assembly_id, name, url = map(str.strip, line.split(',', 2))

        # Filter non-existing wiki pages out
        if 'redlink' in url or 'action=edit' in url:
            continue

        person = None
        try:
            person = Person.query\
                           .filter(Person.name == name)\
                           .join(Candidacy,
                                 Person.id == Candidacy.person_id)\
                           .join(Election,
                                 Election.id == Candidacy.election_id)\
                           .filter(Election.age == assembly_id)\
                           .one()
        except Exception as e:
            print '==', assembly_id, name, url, '=='
            print e

        if not person:
            continue

        op.execute(person_t.update()\
                           .values({
                               'wiki': url,
                           })\
                           .where(person_t.c.id == person.id)
        )


def downgrade():
    op.execute(person_t.update()\
                       .values({
                           'wiki': None
                       })
    )
