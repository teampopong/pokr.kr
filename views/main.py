#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask import redirect, request, render_template, url_for
import re
from sqlalchemy import or_
from werkzeug.local import LocalProxy

from database import db_session
from models.bill import Bill
from models.party import Party
from models.person import Person
from models.region import Region
from models.school import School

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

    @app.route('/search/<query>', methods=['GET'])
    @app.route('/search', methods=['GET'])
    def search(query=''):
        year = request.args.get('year')

        if query:
            people = Person.query.filter(or_(
                         Person.name.like(u'%{0}%'.format(query)),
                         Person.name_en.ilike(u'%{0}%'.format(query))
                     ))
            parties = Party.query.filter(Party.name.like(u'%{0}%'.format(query)))
            schools = School.query.filter(School.name.like(u'%{0}%'.format(query)))
            bills = Bill.query.filter(Bill.name.like(u'%{0}%'.format(query)))
            regions = Region.query.filter(Region.name.like(u'%{0}%'.format(query)))

        elif year:
            people = Person.query.filter_by(birthday_year=year)

        return render_template('search-results.html', **locals())
