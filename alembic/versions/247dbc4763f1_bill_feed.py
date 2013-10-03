"""Bill feed

Revision ID: 247dbc4763f1
Revises: 138c92cb2218
Create Date: 2013-09-30 00:46:20.508375

"""

# revision identifiers, used by Alembic.
revision = '247dbc4763f1'
down_revision = '138c92cb2218'

import re

from alembic import op
import sqlalchemy as sa
from sqlalchemy.types import SchemaType, TypeDecorator, Enum

if sa.__version__ < '0.6.5':
    raise NotImplementedError("Version 0.6.5 or higher of SQLAlchemy is required.")

class EnumSymbol(object):
    """Define a fixed symbol tied to a parent class."""

    def __init__(self, cls_, name, value, description):
        self.cls_ = cls_
        self.name = name
        self.value = value
        self.description = description

    def __reduce__(self):
        """Allow unpickling to return the symbol
        linked to the DeclEnum class."""
        return getattr, (self.cls_, self.name)

    def __iter__(self):
        return iter([self.value, self.description])

    def __repr__(self):
        return "<%s>" % self.name

class EnumMeta(type):
    """Generate new DeclEnum classes."""

    def __init__(cls, classname, bases, dict_):
        cls._reg = reg = cls._reg.copy()
        for k, v in dict_.items():
            if isinstance(v, tuple):
                sym = reg[v[0]] = EnumSymbol(cls, k, *v)
                setattr(cls, k, sym)
        return type.__init__(cls, classname, bases, dict_)

    def __iter__(cls):
        return iter(cls._reg.values())

class DeclEnum(object):
    """Declarative enumeration."""

    __metaclass__ = EnumMeta
    _reg = {}

    @classmethod
    def from_string(cls, value):
        try:
            return cls._reg[value]
        except KeyError:
            raise ValueError(
                    "Invalid value for %r: %r" %
                    (cls.__name__, value)
                )

    @classmethod
    def values(cls):
        return cls._reg.keys()

    @classmethod
    def db_type(cls):
        return DeclEnumType(cls)

class DeclEnumType(SchemaType, TypeDecorator):
    def __init__(self, enum):
        self.enum = enum
        self.impl = Enum(
                        *enum.values(),
                        name="ck%s" % re.sub(
                                    '([A-Z])',
                                    lambda m:"_" + m.group(1).lower(),
                                    enum.__name__)
                    )

    def _set_table(self, table, column):
        self.impl._set_table(table, column)

    def copy(self):
        return DeclEnumType(self.enum)

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return value.value

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return self.enum.from_string(value.strip())



class FeedType(DeclEnum):
    bill = 'B', 'Bill'


def upgrade():
    op.create_table('feed',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', FeedType.db_type(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bill_feed',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('bill_id', sa.Text(), nullable=True),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('proposed_date', sa.Date(), nullable=True),
    sa.Column('sponsor', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['bill_id'], ['bill.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['id'], ['feed.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )

    insert_bill_feed = '''\
CREATE OR REPLACE FUNCTION insert_bill_feed()
RETURNS trigger as $insert_bill_feed_trigger$
DECLARE
    feed_id int;
BEGIN
    INSERT INTO feed ("type") VALUES (
        'B'
    ) RETURNING id INTO feed_id;

    INSERT INTO bill_feed (id, bill_id, name, proposed_date, sponsor) VALUES (
        feed_id,
        NEW.id,
        NEW.name,
        NEW.proposed_date,
        NEW.sponsor
    );

    RETURN NULL;
END;
$insert_bill_feed_trigger$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS insert_bill_feed_trigger ON bill CASCADE;
CREATE TRIGGER insert_bill_feed_trigger
    AFTER INSERT ON bill
    FOR EACH ROW EXECUTE PROCEDURE insert_bill_feed();
'''
    op.execute(insert_bill_feed)


def downgrade():
    op.drop_table('bill_feed')
    op.drop_table('feed')
    op.execute('DROP TYPE ck_feed_type')
