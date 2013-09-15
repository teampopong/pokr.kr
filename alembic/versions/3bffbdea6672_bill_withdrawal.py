"""bill withdrawal

Revision ID: 3bffbdea6672
Revises: 80674dad104
Create Date: 2013-05-21 12:29:13.072828

"""

# revision identifiers, used by Alembic.
revision = '3bffbdea6672'
down_revision = '80674dad104'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('bill_withdrawal',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('person_id', sa.Integer(), nullable=False),
        sa.Column('bill_id', sa.String(length=20), nullable=False),
        sa.ForeignKeyConstraint(['bill_id'], ['bill.id'], ),
        sa.ForeignKeyConstraint(['person_id'], ['person.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('bill_withdrawal')
