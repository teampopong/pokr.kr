#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask import Blueprint, g, redirect, render_template, request, url_for
from utils.conn import get_db
from werkzeug.local import LocalProxy

app = Blueprint('people', __name__,
        template_folder='templates', static_folder='static')
db = LocalProxy(get_db)

# 루트
@app.route('/', methods=['GET'])
def main():
    query = request.args.get('q', None)
    if query is not None:
        return redirect(url_for('people.search', query=query))

    return render_template('person-base.html', menu='people')

# 이름으로 검색
@app.route('/q/<query>', methods=['GET'])
def search(query):
    # TODO: validation & sanitization
    # TODO: 처음엔 몇 개만 받아오고, '더 보기'를 누르면 나머지를 가져옴
    results = list(db['people'].find({
        'name_kr': {'$regex': query}
        }))
    return render_template('search-results.html', menu='people', results=results,
            query=query)

# 사람
@app.route('/<int:id_>', methods=['GET'])
def person(id_):
    person = db['people'].find_one({
        'id': id_
        })

    if person:
        return render_template('person-found.html', menu='people', person=person)
    else:
        return render_template('person-not-found.html', menu='people'), 404
