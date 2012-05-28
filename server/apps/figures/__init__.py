#!/usr/bin/env python

from flask import Blueprint, g

app = Blueprint('figures', __name__)

@app.route('/')
def figures():
    return str(list(g.db['figures'].find()))

@app.route('/<int:id_>')
def figure(id_):
    return str(g.db['figures'].find_one({
        'id': id_
        }))
