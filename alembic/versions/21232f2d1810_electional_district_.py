"""Electional district name for Region table

Revision ID: 21232f2d1810
Revises: 1c61f2fe6ee
Create Date: 2013-12-13 02:23:37.095969

"""

# revision identifiers, used by Alembic.
revision = '21232f2d1810'
down_revision = '1c61f2fe6ee'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('region', sa.Column('district_name', sa.Unicode(), nullable=True))


def downgrade():
    op.drop_column('region', 'district_name')
