"""empty message

Revision ID: 3cea1b2cfa
Revises: 42b10177639f
Create Date: 2013-05-05 17:07:07.392602

"""

# revision identifiers, used by Alembic.
revision = '3cea1b2cfa'
down_revision = '42b10177639f'

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('party', sa.Column('logo', sa.String(length=1024), nullable=True))

def downgrade():
    op.drop_column('party', 'logo')

