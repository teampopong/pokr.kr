#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from datetime import date
import os.path
import re

from flask import abort, current_app, render_template, redirect, request, send_file, url_for
from flask.ext.babel import gettext, format_date
from sqlalchemy.orm import undefer, undefer_group
from sqlalchemy.orm.exc import NoResultFound

from pokr.cache import cache
from pokr.database import db_session
from pokr.models.statement import Statement
from pokr.widgets.year import year
from utils.jinja import breadcrumb


def register(app):
    app.views['statement'] = 'statement_main'
    gettext('statement') # for babel extraction

    @app.route('/statement/', methods=['GET'])
    @breadcrumb(app)
    def statement_main():
        statements = Statement.query
        return render_template('statements.html', statements=statements)


    @app.route('/statement/<id>', methods=['GET'])
    @breadcrumb(app, 'statement')
    def statement(id):
        try:
            statement = Statement.query.filter_by(id=id).one()
        except NoResultFound, e:
            abort(404)

        return render_template('statement.html', statement=statement)
