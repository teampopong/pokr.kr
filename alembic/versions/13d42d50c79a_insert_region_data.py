"""Insert region data

Revision ID: 13d42d50c79a
Revises: 6d11a4b386e
Create Date: 2013-05-11 02:26:20.599269

"""

# revision identifiers, used by Alembic.
revision = '13d42d50c79a'
down_revision = '6d11a4b386e'

from os.path import abspath, dirname, join

from alembic import op
import sqlalchemy as sa


proj_dir = dirname(dirname(dirname(abspath(__file__))))
regions_path = join(proj_dir, 'data/regions.csv')


region_t = sa.sql.table(
    'region',
    sa.sql.column('id', sa.String(length=16)),
    sa.sql.column('name', sa.Unicode(length=20)),
    sa.sql.column('name_cn', sa.Unicode(length=20)),
    sa.sql.column('name_en', sa.String(length=80)),
)


def upgrade():
    for line in list(open(regions_path, 'r'))[1:]:
        code, ko, en, cn = map(str.strip, line.split(','))
        op.execute(region_t.insert().values({
            'id': code,
            'name': ko,
            'name_cn': cn,
            'name_en': en
        }))


def downgrade():
    op.execute(region_t.delete())
