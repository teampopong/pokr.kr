#!/usr/bin/env python

from flask import Blueprint, g

app = Blueprint('people', __name__)

@app.route('/')
def people():
    return str(list(g.db['people'].find()))

@app.route('/<int:id_>')
def person(id_):
    return str(g.db['people'].find_one({
        'id': id_
        }))
