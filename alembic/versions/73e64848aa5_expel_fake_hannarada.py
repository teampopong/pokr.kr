# -*- coding: utf-8 -*-

"""expel fake hannaradang

Revision ID: 73e64848aa5
Revises: 45205c4e6bd8
Create Date: 2013-05-25 13:59:42.784146

"""

from __future__ import unicode_literals

# revision identifiers, used by Alembic.
revision = '73e64848aa5'
down_revision = u'45205c4e6bd8'

from os.path import abspath, dirname, join
import sys

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import and_, desc

parentdir = dirname(dirname(dirname(abspath(__file__))))
sys.path.insert(0,parentdir)
from models.candidacy import Candidacy
from models.party import Party
from models.party_affiliation import party_affiliation


candidacy_t = Candidacy.__table__
party_t = Party.__table__


def upgrade():
    hannara_id = Party.query.filter_by(name='한나라당').one().id
    fannara_id = Party.query.order_by(desc(Party.id)).limit(1).one().id + 1

    # New party
    op.execute(party_t.insert().values({
        'id': fannara_id,
        'name': '한나라당(2012)'
    }))

    for candidacy in Candidacy.query.filter_by(party_id=hannara_id,
                                               age=19):
        # Update party affiliation
        op.execute(party_affiliation.update()\
                         .values({
                             'party_id': fannara_id
                         })\
                         .where(and_(
                             party_affiliation.c.party_id == hannara_id,
                             party_affiliation.c.person_id == candidacy.person_id
                         ))
        )

        # Update candidacy
        op.execute(candidacy_t.update()\
                              .values({
                                  'party_id': fannara_id
                              })\
                              .where(candidacy_t.c.id == candidacy.id)
        )

    update_party_meta()


def downgrade():
    hannara_id = Party.query.filter_by(name='한나라당').one().id
    fannara_id = Party.query.filter_by(name='한나라당(2012)').one().id

    op.execute(party_affiliation.update()\
                     .values({
                         'party_id': hannara_id
                     })\
                     .where(party_affiliation.c.party_id == fannara_id)
    )

    op.execute(candidacy_t.update()\
                          .values({
                              'party_id': hannara_id
                          })\
                          .where(candidacy_t.c.party_id == fannara_id)
    )

    op.execute(party_t.delete().where(party_t.c.id == fannara_id))
    update_party_meta()


def update_party_meta():
    query_update_order = '''update party set "order"=subquery.order from (select row_number() over () as order, * from (select count(person.id) as num_people, max(election.age) as max_age, party.id as party_id from candidacy, election, party, person where candidacy.election_id = election.id and candidacy.person_id = person.id and candidacy.party_id = party.id group by party.id order by max_age desc, num_people desc) as f) as subquery where party.id = subquery.party_id;'''
    op.execute(query_update_order)

    query_update_size = '''update party set size=subquery.size from (select count(distinct(person.id)) as size, party.id as party_id from candidacy, party, person where candidacy.person_id = person.id and candidacy.party_id = party.id group by party.id) as subquery where party.id = subquery.party_id;'''
    op.execute(query_update_size)
