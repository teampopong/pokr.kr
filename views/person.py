#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask import Blueprint, g, redirect, render_template, request, url_for
import time
from utils.conn import get_db
from werkzeug.local import LocalProxy

db = LocalProxy(get_db)

def register(app):

    # 루트
    @app.route('/person/', methods=['GET'])
    def person_main():
        query = request.args.get('q', None)
        if query is not None:
            return redirect(url_for('search', query=query))

        # TODO: 기본 페이지
        return render_template('layout.html')

    # 이름으로 검색
    @app.route('/person/q/<query>', methods=['GET'])
    def search(query):
        # TODO: validation & sanitization
        # TODO: 처음엔 몇 개만 받아오고, '더 보기'를 누르면 나머지를 가져옴
        results = list(db['people'].find({
            'name_kr': {'$regex': query}
            }))
        return render_template('search-results.html', results=results,
                query=query)

    # 사람
    @app.route('/person/<int:id_>', methods=['GET'])
    def person(id_):
        person = get_person(id_)

        if person:
            log_person(id_)
            rivals = get_rivals(person)
            return render_template('person.html', person=person, rivals=rivals)
        else:
            return render_template('not-found.html'), 404

def get_person(id):
    person = db['people'].find_one({
        'id': id
        })
    return person

def get_rivals(person):
    key = 'assembly.%s.district' % person['assembly_no']
    rivals = list(db['people'].find({
        key: person['district']
        }))
    return rivals

def log_person(id):
    db['log_person'].insert({
        'id': id,
        'date': time.time()
    })
