"""Create favorite bill table

Revision ID: 4b1bbdff0b59
Revises: 54b91da358e
Create Date: 2015-05-16 21:49:11.304568

"""

# revision identifiers, used by Alembic.
revision = '4b1bbdff0b59'
down_revision = '54b91da358e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('favorite_bill',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False, index=True),
    sa.Column('bill_id', sa.String(length=20), nullable=False, index=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['bill_id'], ['bill.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'bill_id')
    )

def downgrade():
    op.drop_table('favorite_bill')
