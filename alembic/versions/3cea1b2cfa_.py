"""empty message

Revision ID: 3cea1b2cfa
Revises: 26cc7237b399
Create Date: 2013-05-05 17:07:07.392602

"""

# revision identifiers, used by Alembic.
revision = '3cea1b2cfa'
down_revision = '26cc7237b399'

import json

from os.path import abspath, dirname, join
from alembic import op
import sqlalchemy as sa


proj_dir = dirname(dirname(dirname(abspath(__file__))))
logo_path = join(proj_dir, 'data/party_logos.json')
logo_url_format = 'http://data.popong.com/parties/images/{filename}'

party_t = sa.sql.table(
    'party',
    sa.sql.column('id', sa.String(length=20)),
    sa.sql.column('logo', sa.String(length=1024))
)

def upgrade():
    op.add_column('party', sa.Column('logo', sa.String(length=1024), nullable=True))

    with open(logo_path, 'r') as f:
        logos = json.load(f)

    for id, url in logos.items():
        op.execute(party_t.update()\
                .values({'logo': logo_url_format.format(filename=url)})\
                .where(party_t.c.id==id))

def downgrade():
    op.drop_column('party', 'logo')
