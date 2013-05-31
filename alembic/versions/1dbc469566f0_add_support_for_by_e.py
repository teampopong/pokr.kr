"""Add support for by-election

Revision ID: 1dbc469566f0
Revises: 362b3d8238cf
Create Date: 2013-05-31 09:38:32.951952

"""

# revision identifiers, used by Alembic.
revision = '1dbc469566f0'
down_revision = '362b3d8238cf'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('election', sa.Column('is_regular', sa.Boolean(), nullable=True))


def downgrade():
    op.drop_column('election', 'is_regular')
