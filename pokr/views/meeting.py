#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from datetime import date

from flask import render_template, request
from flask.ext.babel import gettext
from sqlalchemy.orm.exc import NoResultFound

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
        try:
            meeting = Meeting.query.filter_by(id=id).one()
        except NoResultFound, e:
            return render_template('not-found.html'), 404

        return render_template('meeting-dialogue.html', meeting=meeting)
