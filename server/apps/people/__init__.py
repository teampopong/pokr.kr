#!/usr/bin/env python

from flask import Blueprint, g, render_template

app = Blueprint('people', __name__, template_folder='templates', static_folder='static')

@app.route('/')
def people():
    return 'people'
    # return g.db['people'].find()

@app.route('/<int:id_>')
def person(id_):
    person = g.db['people'].find_one({
        'id': id_
        })

    if person:
        return render_template('person-found.html', person=person, menu='people')
    else:
        return render_template('person-not-found.html', menu='people'), 404
