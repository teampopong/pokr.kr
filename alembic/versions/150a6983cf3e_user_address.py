"""User address

Revision ID: 150a6983cf3e
Revises: 28bbad55e1ba
Create Date: 2013-12-01 21:04:24.580618

"""

# revision identifiers, used by Alembic.
revision = '150a6983cf3e'
down_revision = '28bbad55e1ba'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('user', sa.Column('address_id', sa.String(length=16), sa.ForeignKey('region.id'), nullable=True))


def downgrade():
    op.drop_column('user', 'address_id')
