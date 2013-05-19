"""Create indices on the names to be searched

Revision ID: 492245dd3efa
Revises: 433058c55ec3
Create Date: 2013-05-19 14:03:06.580109

"""

# revision identifiers, used by Alembic.
revision = '492245dd3efa'
down_revision = '433058c55ec3'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_index('ix_bill_name', 'bill', ['name'])
    op.create_index('ix_region_name', 'region', ['name'])
    op.create_index('ix_school_name', 'school', ['name'])


def downgrade():
    op.drop_index('ix_bill_name')
    op.drop_index('ix_region_name')
    op.drop_index('ix_school_name')
