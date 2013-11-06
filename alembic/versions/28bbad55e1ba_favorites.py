"""favorites

Revision ID: 28bbad55e1ba
Revises: 1b6b6a7e0ece
Create Date: 2013-09-30 19:08:14.105713

"""

# revision identifiers, used by Alembic.
revision = '28bbad55e1ba'
down_revision = '1b6b6a7e0ece'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('favorite_keyword',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False, index=True),
    sa.Column('keyword_id', sa.Integer(), nullable=False, index=True),
    sa.ForeignKeyConstraint(['keyword_id'], ['keyword.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'keyword_id')
    )
    op.create_table('favorite_person',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False, index=True),
    sa.Column('person_id', sa.Integer(), nullable=False, index=True),
    sa.ForeignKeyConstraint(['person_id'], ['person.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'person_id')
    )


def downgrade():
    op.drop_table('favorite_person')
    op.drop_table('favorite_keyword')
