"""query log table

Revision ID: 8b431ade78d
Revises: 1dbc469566f0
Create Date: 2013-06-16 15:07:38.433484

"""

# revision identifiers, used by Alembic.
revision = '8b431ade78d'
down_revision = '1dbc469566f0'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('query_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('query', sa.UnicodeText(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('query_log')
