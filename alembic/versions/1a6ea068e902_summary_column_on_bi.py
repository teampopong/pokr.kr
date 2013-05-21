"""summary column on bill table

Revision ID: 1a6ea068e902
Revises: 3bffbdea6672
Create Date: 2013-05-21 12:32:15.408610

"""

# revision identifiers, used by Alembic.
revision = '1a6ea068e902'
down_revision = '3bffbdea6672'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('bill', sa.Column('summary', sa.Text(), nullable=True))


def downgrade():
    op.drop_column('bill', 'summary')
