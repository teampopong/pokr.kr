#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import re
from flask import redirect, render_template, url_for
from sqlalchemy.sql.expression import desc

from cache import cache, CACHE_DEFAULT_TIMEOUT
from database import db_session
from models.bill import Bill

year_re = re.compile(r'[1-9][0-9]{3}')

def register(app):

    @app.route('/')
    @cache.cached(CACHE_DEFAULT_TIMEOUT)
    def main():
        return render_template('main.html')

    @app.route('/favicon.ico')
    def favicon():
        return app.send_static_file('images/favicon.ico')

    @app.route('/entity/<keyword>')
    @app.endpoint('entity_page')
    @cache.cached(CACHE_DEFAULT_TIMEOUT)
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

