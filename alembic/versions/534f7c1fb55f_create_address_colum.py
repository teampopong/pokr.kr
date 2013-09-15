"""Create address column in person table

Revision ID: 534f7c1fb55f
Revises: 6d11a4b386e
Create Date: 2013-05-12 14:33:19.490150

"""

# revision identifiers, used by Alembic.
revision = '534f7c1fb55f'
down_revision = '6d11a4b386e'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.add_column('person', sa.Column('address_id', postgresql.ARRAY(sa.String(length=16)), nullable=True))
    op.add_column('person', sa.Column('address', postgresql.ARRAY(sa.Unicode(length=20)), nullable=True))
    op.drop_column('person', u'addr_city')
    op.drop_column('person', u'addr_county')
    op.drop_column('person', u'addr_detail')


def downgrade():
    op.add_column('person', sa.Column(u'addr_detail', sa.VARCHAR(length=80), nullable=True))
    op.add_column('person', sa.Column(u'addr_county', sa.VARCHAR(length=20), nullable=True))
    op.add_column('person', sa.Column(u'addr_city', sa.VARCHAR(length=20), nullable=True))
    op.drop_column('person', 'address')
    op.drop_column('person', 'address_id')
