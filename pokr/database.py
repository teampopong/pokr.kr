from contextlib import contextmanager
from functools import wraps
import os

import alembic.command
from alembic.config import Config as AlembicConfig
from alembic.migration import MigrationContext
from alembic.script import ScriptDirectory
from flask import current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


def get_alembic_config():
    alembic_cfg_path = os.path.join(os.getcwd(), 'alembic.ini')
    alembic_cfg = AlembicConfig(alembic_cfg_path)
    return alembic_cfg


SQLALCHEMY_URI = get_alembic_config().get_main_option('sqlalchemy.url')


class Database(object):
    def __init__(self, app, **kwargs):
        self.app = app
        app.db = self
        self.init_app(app, **kwargs)

    def init_app(self, app, autocommit=False, autoflush=False):
        self.engine = create_engine(SQLALCHEMY_URI)
        self.session = scoped_session(sessionmaker(autocommit=autocommit,
                                                   autoflush=autoflush,
                                                   bind=self.engine))

        if not is_alembic_head(self.app):
            raise AlembicNotOnException()

        self.init_query_property()
        self.init_events()

    def init_events(self):
        @self.app.teardown_request
        def shutdown_session(exception=None):
            self.session.remove()

    def init_query_property(self):
        from popong_models import Base
        Base.query = self.session.query_property()

    def create(self):
        from popong_models import Base
        Base.metadata.create_all(bind=self.engine)

        from social.apps.flask_app.models import init_social
        social_storage = init_social(self.app, Base, self.session)

        alembic.command.stamp(get_alembic_config(), 'head')



@contextmanager
def transaction(**kwargs):
    Session = sessionmaker(bind=current_app.db.engine, **kwargs)
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise


def is_alembic_head(app):
    alembic_cfg = get_alembic_config()
    context = MigrationContext.configure(app.db.session.connection())
    script = ScriptDirectory.from_config(alembic_cfg)
    current_revision = context.get_current_revision()
    head_revision = script.get_current_head()
    return current_revision == head_revision


class AlembicNotOnTheHeadException(Exception):
    pass

