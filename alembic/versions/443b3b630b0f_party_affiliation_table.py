"""party_affiliation table

Revision ID: 443b3b630b0f
Revises: df3415c2347
Create Date: 2014-05-31 02:22:34.753596

"""

# revision identifiers, used by Alembic.
revision = '443b3b630b0f'
down_revision = 'df3415c2347'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('party_affiliation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('person_id', sa.Integer(), nullable=False),
    sa.Column('party_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['party_id'], ['party.id'], ),
    sa.ForeignKeyConstraint(['person_id'], ['person.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_party_affiliation_date'), 'party_affiliation', ['date'], unique=False)
    op.create_index(op.f('ix_party_affiliation_party_id'), 'party_affiliation', ['party_id'], unique=False)
    op.create_index(op.f('ix_party_affiliation_person_id'), 'party_affiliation', ['person_id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_party_affiliation_person_id'), table_name='party_affiliation')
    op.drop_index(op.f('ix_party_affiliation_party_id'), table_name='party_affiliation')
    op.drop_index(op.f('ix_party_affiliation_date'), table_name='party_affiliation')
    op.drop_table('party_affiliation')

