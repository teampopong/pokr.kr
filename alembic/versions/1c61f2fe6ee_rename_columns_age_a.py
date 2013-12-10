"""rename columns: age -> assembly_id

Revision ID: 1c61f2fe6ee
Revises: 4b41bb43626e
Create Date: 2013-12-11 01:55:56.724791

"""

# revision identifiers, used by Alembic.
revision = '1c61f2fe6ee'
down_revision = '4b41bb43626e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column(u'election', u'age', new_column_name=u'assembly_id')
    op.alter_column(u'bill', u'age', new_column_name=u'assembly_id')


def downgrade():
    op.alter_column(u'election', u'assembly_id', new_column_name=u'age')
    op.alter_column(u'bill', u'assembly_id', new_column_name=u'age')
