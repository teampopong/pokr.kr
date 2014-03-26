# TODO: extract from pokr to a separate module

from contextlib import contextmanager
import os

from alembic.config import Config as AlembicConfig
from alembic.migration import MigrationContext
from alembic.script import ScriptDirectory
from alembic import command
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

try:
    from conf.storage import SQLALCHEMY_URI
except ImportError as e:
    import sys
    sys.stderr.write('Error: Update conf/storage.py\n')
    sys.exit(1)


engine = create_engine(SQLALCHEMY_URI)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db(app, login=True):
    if not is_alembic_head():
        raise Exception('alembic is not on the head')

    import pokr.models
    if login:
        from utils.login import init_db; init_db(app)

    Base.metadata.create_all(bind=engine)

    @app.teardown_request
    def shutdown_session(exception=None):
        db_session.remove()


@contextmanager
def transaction(**kwargs):
    Session = sessionmaker(bind=engine, **kwargs)
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise


def is_alembic_head():
    alembic_cfg_path = os.path.join(os.getcwd(), 'alembic.ini')
    alembic_cfg = AlembicConfig(alembic_cfg_path)
    context = MigrationContext.configure(db_session.connection())
    script = ScriptDirectory.from_config(alembic_cfg)
    current_revision = context.get_current_revision()
    head_revision = script.get_current_head()
    return current_revision == head_revision
