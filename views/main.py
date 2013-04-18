#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from database import db_session
from flask import redirect, request, render_template, url_for
import re
from werkzeug.local import LocalProxy
from models.person import Person
from models.party import Party

year_re = re.compile(r'[1-9][0-9]{3}')
party_names = [i[0] for i\
        in db_session.query(Party.name).order_by(Party.order).all()]

def register(app):

    @app.context_processor
    def inject_parties():
        return dict(party_names=party_names)

    @app.context_processor
    def inject_is_pjax():
        is_pjax = request.headers.get('X-PJAX') is not None
        return dict(is_pjax=is_pjax)

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
