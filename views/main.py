#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import getpass
import pickle
import re
import socket

from flask import redirect, render_template, url_for
from sqlalchemy.sql.expression import desc

from database import db_session
from models.bill import Bill

year_re = re.compile(r'[1-9][0-9]{3}')

def register(app):

    with open('data/message.pkl', 'rb') as f:
        message = pickle.load(f)

    if getpass.getuser() in message['id']\
            or socket.gethostname().split('.')[0] in message['hostname']:
        print message['message']
        import sys; sys.exit(1)

    @app.route('/')
    def main():
        return render_template('main.html')

    @app.route('/favicon.ico')
    def favicon():
        return app.send_static_file('images/favicon.ico')

    @app.route('/entity/<keyword>')
    @app.endpoint('entity_page')
    def entity_page(keyword):
        if year_re.match(keyword):
            return redirect(url_for('search', target='people', year=keyword))

        return keyword + u'의 페이지입니다'

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('not-found.html'), 404

    @app.errorhandler(500)
    def internal_error(e):
        return render_template('error.html'), 500

