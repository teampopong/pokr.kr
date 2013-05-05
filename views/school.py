#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask import g, redirect, render_template, request, url_for
from sqlalchemy import or_
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.local import LocalProxy

from database import db_session
from models.person import Person


def register(app):

    # 루트
    @app.route('/school/', methods=['GET'])
    def person_main():
        query = request.args.get('q', None)
        if query is not None:
            return redirect(url_for('search', query=query))

        # TODO: 기본 페이지
        return render_template('layout.html')

    # 학교로 검색
    # FIXME: 별도의 함수로 빼지 말고 통합 검색
    @app.route('/school/<education_id>', methods=['GET'])
    def school(education_id):
        results = Person.query.filter(Person.education_id.any(education_id)).all()
        return render_template('search-results.html', results=results,
                query=education_id)
