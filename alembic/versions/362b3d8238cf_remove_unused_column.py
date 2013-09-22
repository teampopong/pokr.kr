"""Remove unused columns of person table

Revision ID: 362b3d8238cf
Revises: 17b5e9dda9a0
Create Date: 2013-05-31 09:35:58.137604

"""

# revision identifiers, used by Alembic.
revision = '362b3d8238cf'
down_revision = '17b5e9dda9a0'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column('person', u'birth_county')
    op.drop_column('person', u'birth_city')


def downgrade():
    op.add_column('person', sa.Column(u'birth_city', sa.VARCHAR(length=20), nullable=True))
    op.add_column('person', sa.Column(u'birth_county', sa.VARCHAR(length=20), nullable=True))
