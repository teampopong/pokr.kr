"""Remove PartyAffiliation

Revision ID: 138c92cb2218
Revises: 3aecd12384ee
Create Date: 2013-09-28 16:34:40.128374

"""

# revision identifiers, used by Alembic.
revision = '138c92cb2218'
down_revision = '3aecd12384ee'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_table(u'party_affiliation')


def downgrade():
    op.create_table(u'party_affiliation',
    sa.Column(u'id', sa.INTEGER(), nullable=False),
    sa.Column(u'person_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column(u'party_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column(u'start_date', sa.CHAR(length=8), autoincrement=False, nullable=True),
    sa.Column(u'end_date', sa.CHAR(length=8), autoincrement=False, nullable=True),
    sa.Column(u'is_current_member', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['party_id'], [u'party.id'], name=u'party_affiliation_party_id_fkey'),
    sa.ForeignKeyConstraint(['person_id'], [u'person.id'], name=u'party_affiliation_person_id_fkey'),
    sa.PrimaryKeyConstraint(u'id', name=u'party_affiliation_pkey')
    )
