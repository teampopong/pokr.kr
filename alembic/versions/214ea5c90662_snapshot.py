"""Snapshot

Revision ID: 214ea5c90662
Revises: 39f609637ac6
Create Date: 2014-05-31 01:15:13.927175

"""

# revision identifiers, used by Alembic.
revision = '214ea5c90662'
down_revision = '39f609637ac6'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.create_table('snapshot',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tablename', sa.Text(), nullable=False),
    sa.Column('record_id', sa.Text(), nullable=False),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('data', postgresql.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_snapshot_date'), 'snapshot', ['date'], unique=False)
    op.create_index(op.f('ix_snapshot_record_id'), 'snapshot', ['record_id'], unique=False)
    op.create_index(op.f('ix_snapshot_tablename'), 'snapshot', ['tablename'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_snapshot_tablename'), table_name='snapshot')
    op.drop_index(op.f('ix_snapshot_record_id'), table_name='snapshot')
    op.drop_index(op.f('ix_snapshot_date'), table_name='snapshot')
    op.drop_table('snapshot')

