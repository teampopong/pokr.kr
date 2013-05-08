#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask import redirect, render_template, request, url_for
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.local import LocalProxy
from models.party import Party


PAGESIZE = 20


def register(app):

    # 루트
    @app.route('/party/', methods=['GET'])
    def party_main():
        query = request.args.get('q', None)
        offset = int(request.args.get('offset', 0))

        if query is not None:
            return redirect(url_for('party', name=query))

        parties = Party.query.order_by(Party.id)
        return render_template('parties.html', parties=parties, offset=offset,
                pagesize = PAGESIZE)

    # 이름으로 검색
    @app.route('/party/q/<name>', methods=['GET'])
    def party(name):
        try:
            party = Party.query.filter_by(name=name).one()

        except NoResultFound, e:
            return render_template('not-found.html'), 404

        return render_template('party.html', party=party)
