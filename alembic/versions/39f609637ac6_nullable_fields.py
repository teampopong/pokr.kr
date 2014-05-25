"""nullable fields

Revision ID: 39f609637ac6
Revises: 3e683fc1af11
Create Date: 2014-05-25 14:02:04.521397

"""

# revision identifiers, used by Alembic.
revision = '39f609637ac6'
down_revision = u'3e683fc1af11'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column('meeting', 'session_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('meeting', 'sitting_id',
               existing_type=sa.INTEGER(),
               nullable=True)


def downgrade():
    op.alter_column('meeting', 'sitting_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('meeting', 'session_id',
               existing_type=sa.INTEGER(),
               nullable=False)

