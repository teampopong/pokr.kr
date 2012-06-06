#!/usr/bin/env python

from flask import Blueprint, g

app = Blueprint('people', __name__)

@app.route('/')
def people():
    return 'people'
    # return g.db['people'].find()

@app.route('/<int:id_>')
def person(id_):
    return 'person %d' % id_
    '''
    return g.db['people'].find_one({
        'id': id_
        })
    '''
