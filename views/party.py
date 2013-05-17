#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask import redirect, render_template, request, url_for
from flask.ext.babel import gettext
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.expression import desc

from models.party import Party
from utils.jinja import breadcrumb


def register(app):

    app.views['party'] = 'party_main'
    gettext('party') # for babel extraction

    # 루트
    @app.route('/party/', methods=['GET'])
    @breadcrumb(app)
    def party_main():
        query = request.args.get('q', None)

        if query is not None:
            return redirect(url_for('party', name=query))

        parties = Party.query.order_by(desc(Party.id))
        return render_template('parties.html', parties=parties)

    # 이름으로 검색
    @app.route('/party/q/<name>', methods=['GET'])
    @breadcrumb(app, 'party')
    def party(name):
        try:
            party = Party.query.filter_by(name=name).one()

        except NoResultFound, e:
            return render_template('not-found.html'), 404

        return render_template('party.html', party=party)
