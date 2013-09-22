"""empty message

Revision ID: 42b10177639f
Revises: 2f5c5a76269e
Create Date: 2013-05-03 16:18:47.241186

"""

# revision identifiers, used by Alembic.
revision = '42b10177639f'
down_revision = '2f5c5a76269e'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.create_table('bill',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('name', sa.Unicode(length=150), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('proposed_date', sa.Date(), nullable=True),
    sa.Column('decision_date', sa.Date(), nullable=True),
    sa.Column('proposers', postgresql.ARRAY(sa.Unicode(length=100)), nullable=True),
    sa.Column('proposer_representative', sa.Unicode(length=100), nullable=True),
    sa.Column('committee', sa.Unicode(length=100), nullable=True),
    sa.Column('proposer_type', sa.Integer(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('status_detail', sa.Unicode(length=10), nullable=True),
    sa.Column('link_id', sa.String(length=40), nullable=True),
    sa.Column('attachments', postgresql.ARRAY(sa.String(length=1024)), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('bill')
