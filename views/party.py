#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask import redirect, render_template, request, url_for
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.local import LocalProxy
from models.party import Party

def register(app):

    # 루트
    @app.route('/party/', methods=['GET'])
    def party_main():
        query = request.args.get('q', None)
        if query is not None:
            return redirect(url_for('party', name=query))

        # TODO: 정당 목록 나오도록 수정
        return render_template('layout.html')

    # 이름으로 검색
    @app.route('/party/q/<name>', methods=['GET'])
    def party(name):
        try:
            party = Party.query.filter_by(name=name).one()

        except NoResultFound, e:
            return render_template('not-found.html'), 404

        return render_template('party.html', party=party)
