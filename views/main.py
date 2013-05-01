#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask import redirect, render_template, url_for
import re
from werkzeug.local import LocalProxy
from models.person import Person

NUM_RECENT_PEOPLE = 10

year_re = re.compile(r'[1-9][0-9]{3}')

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
        if year_re.match(keyword):
            return redirect(url_for('year', year=keyword))

        return keyword + u'의 페이지입니다'

    @app.route('/year/<year>')
    def year(year):
        results = Person.query.filter_by(birthday_year=year).all()
        return render_template('search-results.html', results=results,
                query=year)

def recent(num_recent_people):
    # FIXME: make this work w/ postgres
    # rp = db['log_person'].find()\
    #         .sort([
    #             ('date', -1)
    #             ])\
    #         .limit(num_recent_people)
    # rp = [get_person(p['id']) for p in rp]
    # return rp
    return []
