"""empty message

Revision ID: 2a31d97fa618
Revises: 4111a95f1719
Create Date: 2013-04-22 14:34:34.913751

"""

# revision identifiers, used by Alembic.
revision = '2a31d97fa618'
down_revision = '4111a95f1719'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('party', sa.Column('size', sa.Integer(), nullable=True))
    query_insert_size = '''update party set size=subquery.size from (select count(distinct(person.id)) as size, party.id as party_id from candidacy, party, person where candidacy.person_id = person.id and candidacy.party_id = party.id group by party.id) as subquery where party.id = subquery.party_id;'''
    op.execute(query_insert_size)


def downgrade():
    op.drop_column('party', 'size')
