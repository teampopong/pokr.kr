#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask import Blueprint, g, redirect, render_template, request, url_for
from utils.conn import get_db
from werkzeug.local import LocalProxy

app = Blueprint('parties', __name__,
        template_folder='templates', static_folder='static')
db = LocalProxy(get_db)

# 루트
@app.route('/', methods=['GET'])
def main():
    query = request.args.get('q', None)
    if query is not None:
        return redirect(url_for('parties.party', name=query))

    # TODO: 정당 목록 나오도록 수정
    return render_template('party-base.html')

# 이름으로 검색
@app.route('/q/<name>', methods=['GET'])
def party(name):
    # TODO: validation & sanitization
    # TODO: 처음엔 몇 개만 받아오고, '더 보기'를 누르면 나머지를 가져옴
    members = list(db['people'].find({
        'party': name
        }))
    party = {
        'name': name,
        'members': members
    }
    if members:
        return render_template('party.html', party=party)
    else:
        return render_template('party-not-found.html'), 404
