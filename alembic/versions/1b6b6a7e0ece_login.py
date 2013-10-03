"""Login

Revision ID: 1b6b6a7e0ece
Revises: 247dbc4763f1
Create Date: 2013-09-30 19:01:04.945577

"""

# revision identifiers, used by Alembic.
revision = '1b6b6a7e0ece'
down_revision = '247dbc4763f1'

import json

from alembic import op
import sqlalchemy as sa
from sqlalchemy.types import PickleType, Text


class JSONType(PickleType):
    impl = Text

    def __init__(self, *args, **kwargs):
        kwargs['pickler'] = json
        super(JSONType, self).__init__(*args, **kwargs)


def upgrade():
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('email', sa.String(length=200), nullable=True),
    sa.Column('name', sa.Unicode(length=40), nullable=True, index=True),
    sa.Column('password', sa.String(length=200), nullable=True),
    sa.Column('username', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('social_auth_usersocialauth',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('provider', sa.String(length=32), nullable=True),
    sa.Column('uid', sa.Unicode(length=255), nullable=True),
    sa.Column('extra_data', JSONType, nullable=True),
    sa.Column('user_id', sa.Integer, nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('provider', 'uid'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id']),
    )
    op.create_table('social_auth_nonce',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('server_url', sa.Unicode(length=255), nullable=True),
    sa.Column('timestamp', sa.Integer, nullable=True),
    sa.Column('salt', sa.Unicode(length=40), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('server_url', 'timestamp', 'salt'),
    )
    op.create_table('social_auth_association',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('server_url', sa.Unicode(length=255), nullable=True),
    sa.Column('handle', sa.Unicode(length=255), nullable=True),
    sa.Column('secret', sa.Unicode(length=255), nullable=True),
    sa.Column('issued', sa.Integer, nullable=True),
    sa.Column('lifetime', sa.Integer, nullable=True),
    sa.Column('assoc_type', sa.Unicode(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('server_url', 'handle'),
    )
    op.create_table('social_auth_code',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.Unicode(length=200), nullable=True),
    sa.Column('code', sa.Unicode(length=32), nullable=True, index=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code', 'email'),
    )


def downgrade():
    op.drop_table('social_auth_usersocialauth')
    op.drop_table('social_auth_nonce')
    op.drop_table('social_auth_association')
    op.drop_table('social_auth_code')
    op.drop_table('user')
