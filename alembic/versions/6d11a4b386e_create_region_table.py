"""Create region table

Revision ID: 6d11a4b386e
Revises: 453b49f6b2b8
Create Date: 2013-05-11 02:25:55.982549

"""

# revision identifiers, used by Alembic.
revision = '6d11a4b386e'
down_revision = '453b49f6b2b8'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('region',
    sa.Column('id', sa.String(length=16), nullable=False),
    sa.Column('name', sa.Unicode(length=20), nullable=False),
    sa.Column('name_cn', sa.Unicode(length=20), nullable=True),
    sa.Column('name_en', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('region')
