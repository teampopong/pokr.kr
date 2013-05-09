#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask import g, redirect, render_template, request, url_for
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.local import LocalProxy
from models.school import School


def register(app): # 루트
    @app.route('/school/', methods=['GET'])
    def school_main():
        query = request.args.get('q', None)

        if query is not None:
            return redirect(url_for('search', query=query))

        schools = School.query.order_by(School.id)
        return render_template('schools.html', schools=schools)

    # 학교로 검색
    # FIXME: 별도의 함수로 빼지 말고 통합 검색
    @app.route('/school/<education_id>', methods=['GET'])
    def school(education_id):
        try:
            school = School.query.filter_by(id=education_id).one()
        except NoResultFound, e:
            return render_template('not-found.html'), 404
        return render_template('school.html', school=school)
