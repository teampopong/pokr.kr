#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask import redirect, render_template, url_for
import re

from database import db_session
from models.party import Party

year_re = re.compile(r'[1-9][0-9]{3}')
party_list = db_session.query(Party.name, Party.size).order_by(Party.order).filter(Party.name != u'무소속')

def register(app):

    @app.context_processor
    def inject_parties():
        return dict(party_list=party_list)

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
            return redirect(url_for('search', year=keyword))

        return keyword + u'의 페이지입니다'

