#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.script import Manager

from database import init_db


fake_app = Flask(__name__)
init_db(fake_app)
manager = Manager(fake_app, with_default_commands=False)


@manager.command
def insert_bills(files):
    from scripts.insert_bills import insert_bills as f
    f(files)


@manager.command
def insert_bill_keywords(files):
    from scripts.insert_bill_keywords import insert_bill_keywords as f
    f(files)


@manager.command
def insert_candidacies(files, age, date):
    from scripts.insert_candidacies import insert_candidacies as f
    f(files, age, date)


if __name__ == '__main__':
    manager.run()
