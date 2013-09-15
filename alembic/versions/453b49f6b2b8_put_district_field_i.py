"""Put district field in candidacy table

Revision ID: 453b49f6b2b8
Revises: 36c44957687f
Create Date: 2013-05-10 17:17:12.342177

"""

# revision identifiers, used by Alembic.
revision = '453b49f6b2b8'
down_revision = '36c44957687f'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def upgrade():
    op.add_column('candidacy', sa.Column('district_id', postgresql.ARRAY(sa.String(length=16)), nullable=True))
    op.add_column('candidacy', sa.Column('district', postgresql.ARRAY(sa.Unicode(length=20)), nullable=True))
    op.drop_column('candidacy', u'region3')
    op.drop_column('candidacy', u'region2')
    op.drop_column('candidacy', u'region1')


def downgrade():
    op.add_column('candidacy', sa.Column(u'region1', sa.VARCHAR(length=20)))
    op.add_column('candidacy', sa.Column(u'region2', sa.VARCHAR(length=20)))
    op.add_column('candidacy', sa.Column(u'region3', sa.VARCHAR(length=4)))
    op.drop_column('candidacy', 'district')
    op.drop_column('candidacy', 'district_id')

