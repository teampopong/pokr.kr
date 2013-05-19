"""Revise bill data structures

Revision ID: 80674dad104
Revises: 492245dd3efa
Create Date: 2013-05-19 21:36:27.076689

"""

# revision identifiers, used by Alembic.
revision = '80674dad104'
down_revision = '492245dd3efa'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


bill_t = sa.sql.table(
    'bill'
)


def upgrade():
    # remove all regacy data
    op.execute(bill_t.delete())

    # new tables
    op.create_table('bill_status',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.Unicode(length=150), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bill_review',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('bill_id', sa.String(length=20), nullable=False),
        sa.Column('name', sa.Unicode(length=150), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=True),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('data', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['bill_id'], ['bill.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cosponsorship',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('person_id', sa.Integer(), nullable=False),
        sa.Column('bill_id', sa.String(length=20), nullable=False),
        sa.Column('is_sponsor', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['bill_id'], ['bill.id'], ),
        sa.ForeignKeyConstraint(['person_id'], ['person.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # changes in bill table
    op.add_column(u'bill', sa.Column('status_ids', postgresql.ARRAY(sa.Integer()), nullable=True))
    op.add_column(u'bill', sa.Column('is_processed', sa.Boolean(), nullable=True))
    op.add_column(u'bill', sa.Column('status_id', sa.Integer(), nullable=False))
    op.add_column(u'bill', sa.Column('sponsor', sa.Unicode(length=40)))
    op.drop_column(u'bill', u'status')
    op.drop_column(u'bill', u'proposer_type')
    op.drop_column(u'bill', u'attachments')
    op.drop_column(u'bill', u'proposer_representative')
    op.drop_column(u'bill', u'status_detail')
    op.drop_column(u'bill', u'proposers')
    op.drop_column(u'bill', u'committee')


def downgrade():
    op.add_column(u'bill', sa.Column(u'committee', sa.VARCHAR(length=100), nullable=True))
    op.add_column(u'bill', sa.Column(u'proposers', postgresql.ARRAY(sa.VARCHAR(length=100)), nullable=True))
    op.add_column(u'bill', sa.Column(u'status_detail', sa.VARCHAR(length=10), nullable=True))
    op.add_column(u'bill', sa.Column(u'proposer_representative', sa.VARCHAR(length=100), nullable=True))
    op.add_column(u'bill', sa.Column(u'attachments', postgresql.ARRAY(sa.VARCHAR(length=1024)), nullable=True))
    op.add_column(u'bill', sa.Column(u'proposer_type', sa.INTEGER(), nullable=True))
    op.add_column(u'bill', sa.Column(u'status', sa.INTEGER(), nullable=True))
    op.drop_column(u'bill', 'status_id')
    op.drop_column(u'bill', 'is_processed')
    op.drop_column(u'bill', 'status_ids')
    op.drop_column(u'bill', 'sponsor')
    op.drop_table('cosponsorship')
    op.drop_table('bill_review')
    op.drop_table('bill_status')
