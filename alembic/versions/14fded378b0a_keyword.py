"""Keyword

Revision ID: 14fded378b0a
Revises: e4e23231a10
Create Date: 2013-06-19 01:07:38.617440

"""

# revision identifiers, used by Alembic.
revision = '14fded378b0a'
down_revision = 'e4e23231a10'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('keyword',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.UnicodeText(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bill_keyword',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('bill_id', sa.String(length=20), nullable=False),
    sa.Column('keyword_id', sa.Integer(), nullable=False),
    sa.Column('weight', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['bill_id'], ['bill.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['keyword_id'], ['keyword.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('bill_id','keyword_id', name='uix_1')
    )


def downgrade():
    op.drop_table('bill_keyword')
    op.drop_table('keyword')
