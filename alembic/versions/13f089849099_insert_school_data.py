"""Insert school data

Revision ID: 13f089849099
Revises: 3cea1b2cfa
Create Date: 2013-05-05 22:58:35.938292

"""

# revision identifiers, used by Alembic.
revision = '13f089849099'
down_revision = '3cea1b2cfa'


from os.path import abspath, dirname, join
from alembic import op
import sqlalchemy as sa


proj_dir = dirname(dirname(dirname(abspath(__file__))))
schools_path = join(proj_dir, 'data/schools.csv')

school_t = sa.sql.table(
    'school',
    sa.sql.column('id', sa.String(length=20)),
    sa.sql.column('name', sa.Unicode(length=100))
)

def upgrade():
    for line in list(open(schools_path, 'r'))[1:]:
        code, ko = map(str.strip, line.split(','))
        op.execute(school_t.insert().values({
            'id': code,
            'name': ko
        }))

def downgrade():
    op.execute(school_t.delete())
