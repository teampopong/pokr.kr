"""rename meeting fields

Revision ID: 2f08fb65fe0b
Revises: 538cda15f3c5
Create Date: 2014-05-24 20:09:08.002797

"""

# revision identifiers, used by Alembic.
revision = '2f08fb65fe0b'
down_revision = '538cda15f3c5'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_index('ix_meeting_parliament', table_name='meeting')
    op.drop_index('ix_meeting_session', table_name='meeting')
    op.drop_index('ix_meeting_sitting', table_name='meeting')
    op.alter_column('meeting', 'session', new_column_name='session_id')
    op.alter_column('meeting', 'parliament', new_column_name='parliament_id')
    op.alter_column('meeting', 'sitting', new_column_name='sitting_id')
    op.create_index(op.f('ix_meeting_parliament_id'), 'meeting', ['parliament_id'], unique=False)
    op.create_index(op.f('ix_meeting_session_id'), 'meeting', ['session_id'], unique=False)
    op.create_index(op.f('ix_meeting_sitting_id'), 'meeting', ['sitting_id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_meeting_sitting_id'), table_name='meeting')
    op.drop_index(op.f('ix_meeting_session_id'), table_name='meeting')
    op.drop_index(op.f('ix_meeting_parliament_id'), table_name='meeting')
    op.alter_column('meeting', 'session_id', new_column_name='session')
    op.alter_column('meeting', 'parliament_id', new_column_name='parliament')
    op.alter_column('meeting', 'sitting_id', new_column_name='sitting')
    op.create_index('ix_meeting_sitting', 'meeting', ['sitting'], unique=False)
    op.create_index('ix_meeting_session', 'meeting', ['session'], unique=False)
    op.create_index('ix_meeting_parliament', 'meeting', ['parliament'], unique=False)

