"""insert values into party_affiliation

Revision ID: 225b82afbf55
Revises: 443b3b630b0f
Create Date: 2014-05-31 02:30:21.664147

"""

# revision identifiers, used by Alembic.
revision = '225b82afbf55'
down_revision = '443b3b630b0f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute("insert into party_affiliation (person_id, party_id, date) select person_id, party_id, to_date(date, 'YYYYMMDD') from candidacy, election where candidacy.election_id = election.id;")


def downgrade():
    op.execute('delete from party_affiliation;')

