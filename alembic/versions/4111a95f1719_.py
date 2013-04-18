"""empty message

Revision ID: 4111a95f1719
Revises: 42dcda5a16ec
Create Date: 2013-04-18 21:35:56.834813

"""

# revision identifiers, used by Alembic.
revision = '4111a95f1719'
down_revision = '42dcda5a16ec'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('party', sa.Column('order', sa.Integer(), nullable=True))
    query_insert_order = '''update party set "order"=subquery.order from (select row_number() over () as order, * from (select count(person.id) as num_people, max(election.age) as max_age, party.id as party_id from candidacy, election, party, person where candidacy.election_id = election.id and candidacy.person_id = person.id and candidacy.party_id = party.id group by party.id order by max_age desc, num_people desc) as f) as subquery where party.id = subquery.party_id;'''
    op.execute(query_insert_order)


def downgrade():
    op.drop_column('party', 'order')
