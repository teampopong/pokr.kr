"""Add 'wiki' field to Person table

Revision ID: 3aecd12384ee
Revises: 3c26b6473d2a
Create Date: 2013-08-19 16:33:39.723178

"""

# revision identifiers, used by Alembic.
revision = '3aecd12384ee'
down_revision = '3c26b6473d2a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('person', sa.Column('wiki', sa.Text(), nullable=True))


def downgrade():
    op.drop_column('person', 'wiki')
