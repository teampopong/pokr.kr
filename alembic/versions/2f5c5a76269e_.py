"""Add education columns to person table

Revision ID: 2f5c5a76269e
Revises: 2a31d97fa618
Create Date: 2013-05-01 23:58:29.411375

"""

# revision identifiers, used by Alembic.
revision = '2f5c5a76269e'
down_revision = '2a31d97fa618'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def upgrade():
    op.add_column('person',\
            sa.Column('education', postgresql.ARRAY(sa.Unicode(60)), nullable=True))
    op.add_column('person',\
            sa.Column('education_id', postgresql.ARRAY(sa.String(20)), nullable=True))


def downgrade():
    op.drop_column('person', 'education_id')
    op.drop_column('person', 'education')
