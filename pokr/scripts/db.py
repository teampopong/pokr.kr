# -*- coding: utf-8 -*-

from alembic import command
from flask import Flask

from pokr.database import Base, engine
from utils.command import Command


class DbCommand(Command):
    __command__ = 'db'


class InitDbCommand(Command):
    __command__ = 'init'
    __parent__ = DbCommand

    @classmethod
    def run(cls, **kwargs):
        dummy_app = Flask(__name__)
        dummy_app.config.from_object('conf.frontend')

        import pokr.models
        from utils.login import init_db; init_db(dummy_app)

        Base.metadata.create_all(bind=engine)

