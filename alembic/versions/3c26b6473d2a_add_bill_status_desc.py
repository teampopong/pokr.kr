"""Add bill status description

Revision ID: 3c26b6473d2a
Revises: 14fded378b0a
Create Date: 2013-06-21 16:47:25.427832

"""

# revision identifiers, used by Alembic.
revision = '3c26b6473d2a'
down_revision = '14fded378b0a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('bill_status', sa.Column('description', sa.UnicodeText(), nullable=True))


def downgrade():
    op.drop_column('bill_status', 'description')
