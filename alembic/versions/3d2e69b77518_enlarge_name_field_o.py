"""Enlarge name, sponsor field of bill table

Revision ID: 3d2e69b77518
Revises: 1a6ea068e902
Create Date: 2013-05-22 11:15:01.534721

"""

# revision identifiers, used by Alembic.
revision = '3d2e69b77518'
down_revision = '1a6ea068e902'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column('bill', 'name', type_=sa.String(256))
    op.alter_column('bill', 'sponsor', type_=sa.String(80))


def downgrade():
    op.alter_column('bill', 'name', type_=sa.String(150))
    op.alter_column('bill', 'sponsor', type_=sa.String(40))
