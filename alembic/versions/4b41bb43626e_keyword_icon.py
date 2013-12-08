"""keyword icon

Revision ID: 4b41bb43626e
Revises: 150a6983cf3e
Create Date: 2013-12-08 14:43:28.682238

"""

# revision identifiers, used by Alembic.
revision = '4b41bb43626e'
down_revision = '150a6983cf3e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('keyword', sa.Column('image', sa.Text(), nullable=True))


def downgrade():
    op.drop_column('keyword', 'image')
