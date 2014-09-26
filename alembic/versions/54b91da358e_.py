"""Alter meeting id columns from integer to string

Revision ID: 54b91da358e
Revises: 40d44f5e7b69
Create Date: 2014-09-26 15:02:36.192223

"""

# revision identifiers, used by Alembic.
revision = '54b91da358e'
down_revision = '40d44f5e7b69'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.alter_column('meeting', 'parliament_id',
               existing_type=sa.INTEGER(),
               type_=sa.Text(),
               existing_nullable=False)
    op.alter_column('meeting', 'session_id',
               existing_type=sa.INTEGER(),
               type_=sa.Text(),
               existing_nullable=True)
    op.alter_column('meeting', 'sitting_id',
               existing_type=sa.INTEGER(),
               type_=sa.Text(),
               existing_nullable=True)


def downgrade():
    op.alter_column('meeting', 'sitting_id',
               existing_type=sa.Text(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    op.alter_column('meeting', 'session_id',
               existing_type=sa.Text(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    op.alter_column('meeting', 'parliament_id',
               existing_type=sa.Text(),
               type_=sa.INTEGER(),
               existing_nullable=False)

