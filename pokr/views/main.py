#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import getpass
import pickle
import re
import socket

from flask import g, redirect, render_template, request, url_for
from sqlalchemy.sql.expression import desc

from pokr.database import db_session
from pokr.models.bill import Bill
from pokr.models.meeting import Meeting
from pokr.models.person import Person
from settings import THIS_ASSEMBLY

year_re = re.compile(r'[1-9][0-9]{3}')

def counts():
    nbills = db_session.query(Bill).count()
    nmeetings = db_session.query(Meeting).count()
    npeople = db_session.query(Person).count()
    return nbills, nmeetings, npeople

def register(app):

    @app.route('/')
    @app.route('/main')
    def main():
        if request.path == '/' and hasattr(g, 'user') and not g.user.is_anonymous():
            return redirect(url_for('mypage'))
        nbills, nmeetings, npeople = counts()
        return render_template('main.html',\
                nbills=nbills, nmeetings=nmeetings, npeople=npeople)

    @app.route('/terms')
    def terms():
        return render_template('terms-of-service.html')

    @app.route('/privacy')
    def privacy():
        return render_template('privacy-policy.html')

    @app.route('/sources')
    def sources():
        return render_template('sources.html')

    @app.route('/favicon.ico')
    def favicon():
        return app.send_static_file('images/favicon.ico')

    @app.route('/sitemap.xml')
    def sitemap():
        return render_template('sitemap.xml')

    @app.route('/entity/<keyword>')
    @app.endpoint('entity_page')
    def entity_page(keyword):
        if year_re.match(keyword):
            return redirect(url_for('search', target='people', year=keyword))

        return keyword + u'의 페이지입니다'

    @app.errorhandler(401)
    def unauthorized(e):
        return render_template('unauthorized.html'), 401

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('not-found.html'), 404

    @app.errorhandler(500)
    def internal_error(e):
        return render_template('error.html'), 500

    @app.context_processor
    def inject_assembly():
        return {
            'THIS_ASSEMBLY': THIS_ASSEMBLY,
        }

    @app.context_processor
    def inject_debug():
            return dict(DEBUG=app.debug)
