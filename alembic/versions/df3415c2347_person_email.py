"""person email

Revision ID: df3415c2347
Revises: 214ea5c90662
Create Date: 2014-05-31 01:36:59.634190

"""

# revision identifiers, used by Alembic.
revision = 'df3415c2347'
down_revision = '214ea5c90662'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('person', sa.Column('email', sa.Text(), nullable=True))


def downgrade():
    op.drop_column('person', 'email')

