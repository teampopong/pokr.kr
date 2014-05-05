# -*- coding: utf-8 -*-

from flask import Flask

from pokr.database import Database
from utils.command import Command


class DbCommand(Command):
    __command__ = 'db'


class InitDbCommand(Command):
    __command__ = 'init'
    __parent__ = DbCommand

    @classmethod
    def run(cls, **kwargs):
        app = Flask(__name__)
        app.config.from_object('settings')
        db = Database(app)
        db.create()

