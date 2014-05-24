#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from datetime import date

from flask import render_template, request
from flask.ext.babel import gettext

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
