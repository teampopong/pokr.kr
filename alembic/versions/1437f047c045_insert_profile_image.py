# -*- coding: utf-8 -*-

from __future__ import unicode_literals

"""Insert profile images from rokps

Revision ID: 1437f047c045
Revises: 4b053946ef00
Create Date: 2013-05-12 17:50:05.449730

"""

# revision identifiers, used by Alembic.
revision = '1437f047c045'
down_revision = '4b053946ef00'

import json
from os.path import abspath, dirname, join
import re
import sys

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import and_

parentdir = dirname(dirname(dirname(abspath(__file__))))
sys.path.insert(0,parentdir)
from models.person import Person

proj_dir = dirname(dirname(dirname(abspath(__file__))))
rokps_path = join(proj_dir, 'data/rokps.json')
number_re = re.compile(r'[0-9]+')


person_t = sa.sql.table(
    'person',
    sa.sql.column('id', sa.Integer),
    sa.sql.column('name', sa.Unicode(length=20)),
    sa.sql.column('image', sa.String(length=1024)),
)


def upgrade():
    with open(rokps_path, 'r') as f:
        people = json.load(f)

    for person in people:
        name = person['성명']
        name = name.split('(', 1)[0].strip()
        birthday_year = person.get('출생-사망') or person.get('생년월일')
        birthday_year = number_re.search(birthday_year).group(0)

        try:
            p = Person.query.filter(and_(Person.name == name,
                                         Person.birthday_year == birthday_year))\
                            .one()

        except Exception, e:
            continue

        op.execute(person_t.update()\
                           .where(person_t.c.id == p.id)
                           .values({
                               person_t.c.image: 'http://data.popong.com/people/images/'+person['id']+'.jpg'
                           })
        )


def downgrade():
    pass
