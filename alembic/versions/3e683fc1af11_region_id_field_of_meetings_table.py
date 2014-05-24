# -*- coding: utf-8 -*-
"""region_id field of 'meetings' table

Revision ID: 3e683fc1af11
Revises: 2f08fb65fe0b
Create Date: 2014-05-24 21:31:25.378918

"""

from __future__ import unicode_literals

# revision identifiers, used by Alembic.
revision = '3e683fc1af11'
down_revision = '2f08fb65fe0b'

from alembic import op
from sqlalchemy.sql import table, column
import sqlalchemy as sa


region = table('region',
    column('id', sa.String(16)),
    column('name', sa.Unicode(20)),
    column('name_en', sa.String(80)),
)


def upgrade():
    op.alter_column('meeting', 'id', type_=sa.BigInteger, autoincrement=False)
    op.alter_column('meeting_attendee', 'meeting_id', type_=sa.BigInteger)
    op.alter_column('statement', 'meeting_id', type_=sa.BigInteger)
    op.add_column('meeting', sa.Column('region_id', sa.String(length=16)))
    op.create_index(op.f('ix_meeting_region_id'), 'meeting', ['region_id'], unique=False)
    op.execute(
        region.insert()\
              .values({
                  'id': '0',
                  'name': '대한민국',
                  'name_en': 'national',
              })
    )


def downgrade():
    op.alter_column('meeting', 'id', type_=sa.Integer, autoincrement=True)
    op.alter_column('meeting_attendee', 'meeting_id', type_=sa.Integer)
    op.alter_column('statement', 'meeting_id', type_=sa.Integer)
    op.drop_index(op.f('ix_meeting_region_id'), table_name='meeting')
    op.drop_column('meeting', 'region_id')
    op.execute(
        region.delete()\
              .where(region.c.id == '0')
    )

