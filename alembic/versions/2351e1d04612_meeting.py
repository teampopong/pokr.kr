"""meeting

Revision ID: 2351e1d04612
Revises: 21232f2d1810
Create Date: 2014-05-21 22:20:28.964038

"""

# revision identifiers, used by Alembic.
revision = '2351e1d04612'
down_revision = '21232f2d1810'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.create_table('meeting',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('committee_id', sa.Text(), nullable=True),
        sa.Column('parliament', sa.Integer(), nullable=False),
        sa.Column('session', sa.Integer(), nullable=False),
        sa.Column('sitting', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('content_json', postgresql.JSON(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_meeting_committee_id'), 'meeting', ['committee_id'], unique=False)
    op.create_index(op.f('ix_meeting_date'), 'meeting', ['date'], unique=False)
    op.create_index(op.f('ix_meeting_parliament'), 'meeting', ['parliament'], unique=False)
    op.create_index(op.f('ix_meeting_session'), 'meeting', ['session'], unique=False)
    op.create_index(op.f('ix_meeting_sitting'), 'meeting', ['sitting'], unique=False)
    op.create_table('statement',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('meeting_id', sa.Integer(), nullable=False),
        sa.Column('person_id', sa.Integer(), nullable=True),
        sa.Column('sequence', sa.Integer(), nullable=False),
        sa.Column('speaker', sa.Text(), nullable=True),
        sa.Column('content', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['meeting_id'], ['meeting.id'], ),
        sa.ForeignKeyConstraint(['person_id'], ['person.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_statement_meeting_id'), 'statement', ['meeting_id'], unique=False)
    op.create_index(op.f('ix_statement_person_id'), 'statement', ['person_id'], unique=False)
    op.create_table('meeting_attendee',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('meeting_id', sa.Integer(), nullable=False),
        sa.Column('person_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['meeting_id'], ['meeting.id'], ),
        sa.ForeignKeyConstraint(['person_id'], ['person.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_meeting_attendee_meeting_id'), 'meeting_attendee', ['meeting_id'], unique=False)
    op.create_index(op.f('ix_meeting_attendee_person_id'), 'meeting_attendee', ['person_id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_meeting_attendee_person_id'), table_name='meeting_attendee')
    op.drop_index(op.f('ix_meeting_attendee_meeting_id'), table_name='meeting_attendee')
    op.drop_table('meeting_attendee')
    op.drop_index(op.f('ix_statement_person_id'), table_name='statement')
    op.drop_index(op.f('ix_statement_meeting_id'), table_name='statement')
    op.drop_table('statement')
    op.drop_index(op.f('ix_meeting_sitting'), table_name='meeting')
    op.drop_index(op.f('ix_meeting_session'), table_name='meeting')
    op.drop_index(op.f('ix_meeting_parliament'), table_name='meeting')
    op.drop_index(op.f('ix_meeting_date'), table_name='meeting')
    op.drop_index(op.f('ix_meeting_committee_id'), table_name='meeting')
    op.drop_table('meeting')

