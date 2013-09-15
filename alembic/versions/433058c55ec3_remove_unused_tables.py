"""Remove unused tables

Revision ID: 433058c55ec3
Revises: 4b053946ef00
Create Date: 2013-05-19 13:46:15.413440

"""

# revision identifiers, used by Alembic.
revision = '433058c55ec3'
down_revision = '534f7c1fb55f'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.drop_table(u'experience')
    op.drop_table(u'education')


def downgrade():
    op.create_table(u'education',
    sa.Column(u'id', sa.INTEGER(), server_default="nextval('education_id_seq'::regclass)", nullable=False),
    sa.Column(u'person_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column(u'school_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column(u'course', postgresql.ENUM(u'elementary', u'middle', u'high', u'undergrad', u'grad', name=u'enum_education_course'), autoincrement=False, nullable=True),
    sa.Column(u'mayor', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column(u'start_year', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column(u'end_year', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column(u'status', postgresql.ENUM(u'in', u'dropped', u'graduated', u'completed', name=u'enum_education_status'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['person_id'], [u'person.id'], name=u'education_person_id_fkey'),
    sa.ForeignKeyConstraint(['school_id'], [u'school.id'], name=u'education_school_id_fkey'),
    sa.PrimaryKeyConstraint(u'id', name=u'education_pkey')
    )
    op.create_table(u'experience',
    sa.Column(u'id', sa.INTEGER(), server_default="nextval('experience_id_seq'::regclass)", nullable=False),
    sa.Column(u'person_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column(u'institution', sa.VARCHAR(length=60), autoincrement=False, nullable=True),
    sa.Column(u'position', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column(u'start_date', sa.CHAR(length=8), autoincrement=False, nullable=True),
    sa.Column(u'end_date', sa.CHAR(length=8), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['person_id'], [u'person.id'], name=u'experience_person_id_fkey'),
    sa.PrimaryKeyConstraint(u'id', name=u'experience_pkey')
    )
