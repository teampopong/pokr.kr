"""add original document url field to bill table

Revision ID: e4e23231a10
Revises: 8b431ade78d
Create Date: 2013-06-16 17:30:43.020409

"""

# revision identifiers, used by Alembic.
revision = 'e4e23231a10'
down_revision = '8b431ade78d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('bill', sa.Column('document_url', sa.Text(), nullable=True))


def downgrade():
    op.drop_column('bill', 'document_url')
