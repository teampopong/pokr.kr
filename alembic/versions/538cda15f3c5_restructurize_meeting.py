"""restructurize meeting

Revision ID: 538cda15f3c5
Revises: 31f80d1b5621
Create Date: 2014-05-24 14:49:42.114336

"""

# revision identifiers, used by Alembic.
revision = '538cda15f3c5'
down_revision = '31f80d1b5621'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.add_column('meeting', sa.Column('committee', sa.Text(), nullable=True))
    op.add_column('meeting', sa.Column('dialogue', postgresql.JSON(), nullable=True))
    op.add_column('meeting', sa.Column('issues', postgresql.ARRAY(sa.Text()), nullable=True))
    op.add_column('meeting', sa.Column('pdf_url', sa.Text(), nullable=True))
    op.add_column('meeting', sa.Column('url', sa.Text(), nullable=True))
    op.drop_index('ix_meeting_committee_id', table_name='meeting')
    op.drop_column('meeting', 'content_json')
    op.drop_column('meeting', 'committee_id')
    op.create_index(op.f('ix_meeting_committee'), 'meeting', ['committee'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_meeting_committee'), table_name='meeting')
    op.add_column('meeting', sa.Column('committee_id', sa.TEXT(), autoincrement=False, nullable=True))
    op.add_column('meeting', sa.Column('content_json', postgresql.JSON(), autoincrement=False, nullable=True))
    op.create_index('ix_meeting_committee_id', 'meeting', ['committee_id'], unique=False)
    op.drop_column('meeting', 'url')
    op.drop_column('meeting', 'pdf_url')
    op.drop_column('meeting', 'issues')
    op.drop_column('meeting', 'dialogue')
    op.drop_column('meeting', 'committee')

