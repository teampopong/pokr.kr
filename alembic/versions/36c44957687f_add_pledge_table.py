"""Add pledge table

Revision ID: 36c44957687f
Revises: 3cea1b2cfa
Create Date: 2013-05-07 17:12:20.111941

"""

# revision identifiers, used by Alembic.
revision = '36c44957687f'
down_revision = '3cea1b2cfa'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('pledge',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('candidacy_id', sa.Integer(), nullable=False),
    sa.Column('pledge', sa.Unicode(length=128), nullable=True),
    sa.Column('description', sa.UnicodeText(), nullable=True),
    sa.ForeignKeyConstraint(['candidacy_id'], ['candidacy.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('pledge')
