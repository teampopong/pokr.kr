#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask import Blueprint, g, redirect, render_template, request, url_for
from database import db_session
import json
from models.person import Person
from sqlalchemy.orm.exc import NoResultFound
import time
from werkzeug.local import LocalProxy

person_names_json = json.dumps([i[0] for i in db_session.query(Person.name.distinct())])

def register(app):

    # 루트
    @app.route('/person/', methods=['GET'])
    def person_main():
        query = request.args.get('q', None)
        if query is not None:
            return redirect(url_for('search', query=query))

        # TODO: 기본 페이지
        return render_template('layout.html')

    @app.route('/person/all-names.json', methods=['GET'])
    def person_all_names():
        return person_names_json

    # 이름으로 검색
    @app.route('/person/q/<query>', methods=['GET'])
    def search(query):
        # TODO: validation & sanitization
        # TODO: 처음엔 몇 개만 받아오고, '더 보기'를 누르면 나머지를 가져옴
        results = Person.query.filter(Person.name.like(u'%{0}%'.format(query))).all()
        return render_template('search-results.html', results=results,
                query=query)

    # 사람
    @app.route('/person/<int:id>', methods=['GET'])
    def person(id):
        try:
            person = Person.query.filter_by(id=id).one()
        except NoResultFound, e:
            return render_template('not-found.html'), 404

        try:
            person_extra_vars = json.loads(person.extra_vars)
            if not isinstance(person_extra_vars.get('experience', None), list):
                person_extra_vars['experience'] = [person_extra_vars['experience']]
        except ValueError, e:
            pass

        log_person(id)
        # XXX: script tag가 포함되어 있으면 pjax 불가
        return render_template('person.html', person=person,
                person_extra_vars=person_extra_vars, is_pjax=False)

def log_person(id):
    # FIXME: make this work w/ postgres
    # db['log_person'].insert({
    #     'id': id,
    #     'date': time.time()
    # })
    pass
