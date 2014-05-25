#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from datetime import date
import os.path

from flask import current_app, render_template, request
from flask.ext.babel import gettext
from sqlalchemy.orm.exc import NoResultFound

from pokr.cache import cache
from pokr.models.meeting import Meeting
from pokr.widgets.year import year
from utils.jinja import breadcrumb


def register(app):
    app.views['meeting'] = 'meeting_main'
    gettext('meeting') # for babel extraction

    @app.route('/meeting/', methods=['GET'])
    @breadcrumb(app)
    def meeting_main():
        year = request.args.get('year', date.today().year)
        return render_template(\
                'meetings.html', year=int(year))

    @app.route('/meeting/<id>/', methods=['GET'])
    @breadcrumb(app, 'meeting')
    def meeting(id):
        try:
            meeting = Meeting.query.filter_by(id=id).one()
        except NoResultFound, e:
            return render_template('not-found.html'), 404

        return render_template('meeting.html', meeting=meeting)

    @app.route('/meeting/<id>/dialog', methods=['GET'])
    def meeting_dialogue(id):
        glossary_js = generate_glossary_js()
        try:
            meeting = Meeting.query.filter_by(id=id).one()
        except NoResultFound, e:
            return render_template('not-found.html'), 404

        return render_template('meeting-dialogue.html',\
                meeting=meeting, glossary_js=glossary_js)

@cache.memoize(timeout=60*60*24)
def generate_glossary_js():
    datadir = os.path.join(current_app.root_path, 'data')
    terms_regex = open('%s/glossary-terms.regex' % datadir).read().decode('utf-8').strip()
    dictionary = open('%s/glossary-map.json' % datadir).read().decode('utf-8').strip()
    return render_template('js/glossary.js', terms_regex=terms_regex,
            dictionary=dictionary)
