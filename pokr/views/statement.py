#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from datetime import date
import os.path
import re

from flask import abort, current_app, render_template, redirect, request, send_file, url_for
from flask.ext.babel import gettext, format_date
from sqlalchemy import and_
from sqlalchemy.orm import undefer, undefer_group
from sqlalchemy.orm.exc import NoResultFound

from pokr.cache import cache
from pokr.database import db_session
from pokr.models.statement import Statement
from pokr.views.meeting import generate_glossary_js
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
        glossary_js = generate_glossary_js()
        try:
            statement = Statement.query.filter_by(id=id).one()
        except NoResultFound, e:
            abort(404)

        before_statement = Statement.query.filter(and_(\
                Statement.meeting_id==statement.meeting_id,
                Statement.sequence==statement.sequence - 1)).first()

        next_statement = Statement.query.filter(and_(\
                Statement.meeting_id==statement.meeting_id,
                Statement.sequence==statement.sequence + 1)).first()

        return render_template('statement.html', statement=statement,\
                before=before_statement, next=next_statement,
                glossary_js=glossary_js)
