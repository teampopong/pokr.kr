import os.path

from alembic.config import Config as AlembicConfig
from alembic import command
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import settings


alembic_cfg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                'alembic.ini')
engine = create_engine(settings.sqlalchemy_uri)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db(app):
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    Base.metadata.create_all(bind=engine)

    alembic_cfg = AlembicConfig(alembic_cfg_path)
    command.upgrade(alembic_cfg, 'head')

    @app.teardown_request
    def shutdown_session(exception=None):
        db_session.remove()
