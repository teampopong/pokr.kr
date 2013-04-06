"""create extra_vars field at person table

Revision ID: 42dcda5a16ec
Revises: None
Create Date: 2013-04-06 19:54:40.244663

"""

# revision identifiers, used by Alembic.
revision = '42dcda5a16ec'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('person', sa.Column('extra_vars', sa.Text))


def downgrade():
    op.drop_column('person', 'extra_vars')
