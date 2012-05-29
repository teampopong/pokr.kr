#!/usr/bin/env python

from flask import Blueprint, g
from utils import response_json

app = Blueprint('people', __name__)

@app.route('/')
@response_json
def people():
    return g.db['people'].find()

@app.route('/<int:id_>')
@response_json
def person(id_):
    return g.db['people'].find_one({
        'id': id_
        })
