#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask import redirect, url_for
from views.person import get_person
from utils.conn import get_db
from werkzeug.local import LocalProxy

NUM_RECENT_PEOPLE = 10

db = LocalProxy(get_db)

def register(app):

    @app.context_processor
    def inject_recent():
        rp = recent(NUM_RECENT_PEOPLE)
        return dict(recent_people=rp)

    @app.route('/')
    def main():
        return redirect(url_for('person_main'))

    @app.route('/favicon.ico')
    def favicon():
        return app.send_static_file('images/favicon.ico')

    @app.route('/entity/<keyword>')
    @app.endpoint('entity_page')
    def entity_page(keyword):
        return keyword + u'의 페이지입니다'

def recent(num_recent_people):
    rp = db['log_person'].find()\
            .sort([
                ('date', -1)
                ])\
            .limit(num_recent_people)
    rp = [get_person(p['id']) for p in rp]
    return rp
